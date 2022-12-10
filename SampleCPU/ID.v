`include "lib/defines.vh"
module ID(
    input wire clk,
    input wire rst,
    // input wire flush,
    input wire [`StallBus-1:0] stall,
    
    input wire ex_is_load,
    
    output wire stallreq,

    input wire [`IF_TO_ID_WD-1:0] if_to_id_bus,

    input wire [31:0] inst_sram_rdata,

    input wire [`WB_TO_RF_WD-1:0] wb_to_rf_bus,
    input wire [37:0] ex_to_id,
    input wire [37:0] mem_to_id,
    input wire [37:0] wb_to_id,
    output wire [`ID_TO_EX_WD-1:0] id_to_ex_bus,
    output wire [`BR_WD-1:0] br_bus,
    output wire stallreq_from_id
);

    reg [`IF_TO_ID_WD-1:0] if_to_id_bus_r;
    wire [31:0] inst;
    wire [31:0] id_pc;
    wire ce;
    
    wire wb_rf_we;
    wire [4:0] wb_rf_waddr;
    wire [31:0] wb_rf_wdata;
    wire wb_id_we;
    wire [4:0] wb_id_waddr;
    wire [31:0] wb_id_wdata;
    wire mem_id_we;
    wire [4:0] mem_id_waddr;
    wire [31:0] mem_id_wdata;
    wire ex_id_we;
    wire [4:0] ex_id_waddr;
    wire [31:0] ex_id_wdata;
    always @ (posedge clk) begin
        if (rst) begin
            if_to_id_bus_r <= `IF_TO_ID_WD'b0;        
        end
        // else if (flush) begin
        //     ic_to_id_bus <= `IC_TO_ID_WD'b0;
        // end
        else if (stall[1]==`Stop && stall[2]==`NoStop) begin
            if_to_id_bus_r <= `IF_TO_ID_WD'b0;
        end
        else if (stall[1]==`NoStop) begin
            if_to_id_bus_r <= if_to_id_bus;
        end
    end
    reg q;
    always @(posedge clk) begin
        if (stall[1]==`Stop) begin
            q = 1'b1;
            q <= 1'b1;
        end
        else begin
            q = 1'b0;
            q <= 1'b0;
        end
    end
    assign inst = (q) ?inst: inst_sram_rdata;
@@ -182,7 +182,13 @@ module ID(
    inst_xor,//寄存器 rs 中的值与寄存器 rt 中的值按位逻辑异或，结果写入寄存器 rd 中。
    inst_xori,//寄存器 rs 中的值与 0 扩展至 32 位的立即数 imm 按位逻辑异或，结果写入寄存器 rt 中。
    inst_nor,//寄存器 rs 中的值与寄存器 rt 中的值按位逻辑或非，结果写入寄存器 rd 中。
    inst_sw;//将 base 寄存器的值加上符号扩展后的立即数 offset 得到访存的虚地址，据此虚地址将 rt 寄存器的值存入内存中。
    inst_sw,//将 base 寄存器的值加上符号扩展后的立即数 offset 得到访存的虚地址，据此虚地址将 rt 寄存器的值存入内存中。
    inst_sltu,//将寄存器 rs 的值与寄存器 rt 中的值进行无符号数比较，如果寄存器 rs 中的值小，则寄存器rd置1,否则寄存器 rd 置0。
    inst_slt,//将寄存器 rs 的值与寄存器 rt 中的值进行有符号数比较，如果寄存器 rs 中的值小，则寄存器 rd 置1否则寄存器rd置0。
    inst_slti,//将寄存器 rs 的值与有符号扩展至 32 位的立即数 imm 进行有符号数比较,如果寄存器 rs 中的值小，则寄存器 rt置1；否则寄存器 rt置0。
    inst_sltiu;//将寄存器 rs 的值与有符号扩展至 32 位的立即数 imm 进行无符号数比较，如果寄存器 rs 中的值
               //小，则寄存器 rt 置 1；否则寄存器 rt 置 0


    wire op_add, op_sub, op_slt, op_sltu;
    wire op_and, op_nor, op_or, op_xor;
@@ -225,10 +231,15 @@ module ID(
    assign inst_xori    = op_d[6'b00_1110];
    assign inst_nor     = op_d[6'b00_0000] && func_d[6'b10_0111];
    assign inst_sw      = op_d[6'b10_1011];
    assign inst_sltu    = op_d[6'b00_0000] && func_d[6'b10_1011];
    assign inst_slt     = op_d[6'b00_0000] && func_d[6'b10_1010];
    assign inst_slti    = op_d[6'b00_1010];
    assign inst_sltiu   = op_d[6'b00_1011];

    // rs to reg1
    assign sel_alu_src1[0] =  inst_nor | inst_xori | inst_sw | inst_xor | inst_ori | inst_addiu |
                              inst_subu | inst_jr | inst_lw | inst_addu | inst_or;
                              inst_subu|  inst_jr  | inst_lw | inst_addu| inst_or  | inst_sltu  | 
                              inst_slt | inst_slti |inst_sltiu;

    // pc to reg1
    assign sel_alu_src1[1] = inst_jal;
@@ -238,10 +249,11 @@ module ID(


    // rt to reg2
    assign sel_alu_src2[0] =inst_nor | inst_xor  | inst_subu | inst_addu | inst_or | inst_sll;
    assign sel_alu_src2[0] =inst_nor | inst_xor  | inst_subu | inst_addu | inst_or | inst_sll | inst_sltu 
                                     | inst_slt;

    // imm_sign_extend to reg2
    assign sel_alu_src2[1] = inst_lui | inst_addiu | inst_lw | inst_sw;
    assign sel_alu_src2[1] = inst_lui | inst_addiu | inst_lw | inst_sw | inst_slti |inst_sltiu;

    // 32'b8 to reg2
    assign sel_alu_src2[2] = inst_jal;
@@ -253,8 +265,8 @@ module ID(

    assign op_add = inst_addiu | inst_lw | inst_addu | inst_jal | inst_sw;
    assign op_sub = inst_subu;
    assign op_slt = 1'b0;
    assign op_sltu = 1'b0;
    assign op_slt = inst_slt | inst_slti; //有符号比较
    assign op_sltu = inst_sltu|inst_sltiu;  //无符号比较
    assign op_and = 1'b0;
    assign op_nor = inst_nor;
    assign op_or = inst_ori | inst_or;
@@ -270,23 +282,24 @@ module ID(



    // load and store enable
    // mem load and store enable
    assign data_ram_en = inst_lw | inst_sw ;

    // write enable
    // mem write enable
    assign data_ram_wen = inst_lw ? 4'b0000: inst_sw ? 4'b1111 : 4'b0000;


    // regfile store enable
    assign rf_we =inst_nor |inst_xori | inst_xor | inst_sll | inst_ori | inst_lui | 
                inst_addiu | inst_subu | inst_jal | inst_lw | inst_addu | inst_or ;
                inst_addiu | inst_subu | inst_jal | inst_lw | inst_addu | inst_or | 
                inst_sltu  | inst_slt | inst_slti |inst_sltiu;



    // store in [rd]
    assign sel_rf_dst[0] =inst_nor | inst_xor | inst_subu | inst_addu | inst_or | inst_sll;
    assign sel_rf_dst[0] =inst_nor | inst_xor | inst_subu | inst_addu | inst_or | inst_sll | inst_sltu | inst_slt;
    // store in [rt] 
    assign sel_rf_dst[1] =inst_xori | inst_ori | inst_lui | inst_addiu | inst_lw ;
    assign sel_rf_dst[1] =inst_xori | inst_ori | inst_lui | inst_addiu | inst_lw | inst_slti |inst_sltiu;
    // store in [31]
    assign sel_rf_dst[2] = inst_jal;

    // sel for regfile address
    assign rf_waddr = {5{sel_rf_dst[0]}} & rd 
                    | {5{sel_rf_dst[1]}} & rt
                    | {5{sel_rf_dst[2]}} & 32'd31;
    
    // 0 from alu_res ; 1 from ld_res
    assign sel_rf_res = 1'b0; 
    assign id_to_ex_bus = {
        id_pc,          // 158:127
        inst,           // 126:95
        alu_op,         // 94:83
        sel_alu_src1,   // 82:80
        sel_alu_src2,   // 79:76
        data_ram_en,    // 75
        data_ram_wen,   // 74:71
        rf_we,          // 70
        rf_waddr,       // 69:65
        sel_rf_res,     // 64
        rdata11,         // 63:32
        rdata22          // 31:0
    };
    wire br_e;
    wire [31:0] br_addr;
    wire rs_eq_rt;
    wire rs_ge_z;
    wire rs_gt_z;
    wire rs_le_z;
    wire rs_lt_z;
    wire [31:0] pc_plus_4;
    assign pc_plus_4 = id_pc + 32'h4;
 
    assign rs_eq_rt = (rdata11 == rdata22);
    assign br_e = (inst_beq & rs_eq_rt) | inst_jr | inst_jal | (inst_bne & !rs_eq_rt);
    assign br_addr = inst_beq ? (pc_plus_4 + {{14{inst[15]}},inst[15:0],2'b0}) 
                    :inst_jr  ? (rdata11)  
                    :inst_jal ? ({pc_plus_4[31:28],inst[25:0],2'b0}) 
                    :inst_bne ? (pc_plus_4+{{14{inst[15]}},{inst[15:0],2'b00}}) : 32'b0;
    assign br_bus = {
        br_e,
        br_addr
    };
     
    assign stallreq_from_id = (ex_is_load  & ex_id_waddr == rs) | (ex_is_load & ex_id_waddr == rt) ;
    
endmodule