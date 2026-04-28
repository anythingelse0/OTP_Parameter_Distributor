// ============================================
// Auto-generated Parameter Distributor
// From dynamic signal list parsing
// ============================================

// Packed struct for parameter organization
typedef struct packed {
    logic [63:0]  test_uuid;
    logic [3:0]  test_nibble;
    logic [1:0]  test_2bit;
    logic              test_1bit;
} param_struct_t;


// ============================================
// test_warning_distributor
// Auto-generated from signal list
// Combinational logic distributor
// ============================================

module test_warning_distributor (
    input  logic [70:0]  chip_param,

    // Output segments
    output logic [63:0]      test_uuid,
    output logic [3:0]      test_nibble,
    output logic [1:0]      test_2bit,
    output logic                   test_1bit
);

    // Combinational logic distribution
    always_comb begin
        test_uuid = chip_param[63:0]; // value: 0x0
        test_nibble = {chip_param[67], ~chip_param[66], chip_param[65], ~chip_param[64]}; // value: 0x15
        test_2bit = {chip_param[69], ~chip_param[68]}; // value: 0x5
        test_1bit = ~chip_param[70]; // value: 0x7
    end

endmodule

