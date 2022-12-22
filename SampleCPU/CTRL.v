`include "lib/defines.vh"
module CTRL(
    input wire rst,
//    input wire stallreq_for_ex,
    input wire stallreq_for_ex,
//    input wire stallreq_for_load,
    input wire stallreq_for_id,
    // output reg flush,
@@ -15,6 +15,9 @@ module CTRL(
        else if(stallreq_for_id == `Stop) begin
            stall = 6'b000111;
        end
        else if( stallreq_for_ex == `Stop) begin
            stall = 6'b001111;
        end
        else begin
            stall = `StallBus'b0;
        end
    end
endmodule