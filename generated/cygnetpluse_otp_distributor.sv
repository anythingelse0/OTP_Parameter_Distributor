// ============================================
// Auto-generated Parameter Distributor
// From dynamic signal list parsing
// ============================================

// Packed struct for parameter organization
typedef struct packed {
    logic [63:0]  uuid;
    logic [15:0]  chip_id;
    logic [3:0]  version_id;
    logic [5:0]  bias_res_calib_e;
    logic              en_res_calib_e;
    logic [3:0]  model_id_e;
    logic [15:0]  temp_value_ref_e;
    logic [12:0]  duty_cycle_ref_e;
    logic [10:0]  one_over_k_e;
    logic              efuse_val_csr_cfg_xtal_div2_en;
    logic              efuse_val_csr_digpll_cfg_cp_current_from;
    logic              efuse_val_csr_digpll_cfg_r3;
    logic              efuse_val_csr_digpll_en_vco_bias_lpf;
    logic              efuse_val_csr_digpll_ensw_vco_core;
    logic              efuse_val_csr_digpll_ensw_vco_pre;
    logic              efuse_val_csr_digpll_inner_ldo_en;
    logic              efuse_val_csr_xtal_div2_en;
    logic              efuse_val_csr_xtal_div2_en_ana;
    logic              efuse_val_csr_xtal_ldo09_en;
    logic              efuse_val_csr_xtal_ldo26_en;
    logic [1:0]  efuse_val_csr_digpll_cfg_bias_vco;
    logic [1:0]  efuse_val_csr_digpll_cfg_c1;
    logic [1:0]  efuse_val_csr_digpll_cfg_c2;
    logic [1:0]  efuse_val_csr_digpll_cfg_ldo_vsel;
    logic [1:0]  efuse_val_csr_digpll_cfg_r2;
    logic [2:0]  efuse_val_csr_digpll_cfg_cp_current;
    logic [2:0]  efuse_val_csr_digpll_cfg_vco_band;
    logic [2:0]  efuse_val_csr_digpll_cfg_vco_up;
    logic [2:0]  efuse_val_csr_xtal_ldo09_vsel;
    logic [2:0]  efuse_val_csr_xtal_ldo26_vsel;
    logic [3:0]  efuse_val_csr_digpll_bias_ext;
    logic [3:0]  efuse_val_csr_digpll_bias_int;
    logic              efuse_val_csr_10g_sds_pll_band_en;
    logic              efuse_val_csr_12g_sds_pll_band_en;
    logic [3:0]  efuse_val_csr_c16_ki_c2_cors;
    logic [3:0]  efuse_val_csr_c16_ki_c2_fine;
    logic [2:0]  efuse_val_csr_c16_ki_coe_cors;
    logic [2:0]  efuse_val_csr_c16_ki_coe_fine;
    logic [3:0]  efuse_val_csr_cdr_c1_c20;
    logic [3:0]  efuse_val_csr_cdr_c1_c20_fine;
    logic [3:0]  efuse_val_csr_cdr_c1_c32;
    logic [3:0]  efuse_val_csr_cdr_c1_c32_fine;
    logic [3:0]  efuse_val_csr_cdr_c2_c20;
    logic [3:0]  efuse_val_csr_cdr_c2_c20_fine;
    logic [3:0]  efuse_val_csr_cdr_c2_c32;
    logic [3:0]  efuse_val_csr_cdr_c2_c32_fine;
    logic [7:0]  efuse_val_csr_cdr_lock_tm_lpwr;
    logic [8:0]  efuse_val_csr_csr_c16_kp_out;
    logic              efuse_val_csr_en_pcie_lp;
    logic [6:0]  efuse_val_csr_eod_height_rect;
    logic [6:0]  efuse_val_csr_eod_height_tri;
    logic              efuse_val_csr_eod_shape_tri_rect;
    logic [5:0]  efuse_val_csr_eod_wth_rect;
    logic [5:0]  efuse_val_csr_eod_wth_tri;
    logic [3:0]  efuse_val_csr_sigdet_loss_to;
    logic              efuse_val_csr_man_sds_afe_ctle_peak_en;
    logic              efuse_val_csr_man_sds_afe_pga_gain_en;
    logic [3:0]  efuse_val_csr_sds_pll_vcoldo_vtune;
    logic              efuse_val_csr_sds_pll_vcoldo_en_ext;
    logic              efuse_val_csr_sds_pll_vcoldo_en;
    logic [3:0]  efuse_val_csr_sds_pll_vco_sel_vco2_current;
    logic [5:0]  efuse_val_csr_sds_pll_vco_iptat;
    logic [5:0]  efuse_val_csr_sds_pll_vco_iconstant;
    logic [1:0]  efuse_val_csr_sds_pll_pllldo_vtune;
    logic              efuse_val_csr_sds_pll_pllldo_en_ext;
    logic              efuse_val_csr_sds_pll_pllldo_en;
    logic [3:0]  efuse_val_csr_sds_pll_pdivn_s;
    logic [9:0]  efuse_val_csr_sds_pll_pdivn_p;
    logic [3:0]  efuse_val_csr_sds_pll_fdivn_s;
    logic [9:0]  efuse_val_csr_sds_pll_fdivn_p;
    logic [3:0]  efuse_val_csr_sds_pll_bias_sel_iptat;
    logic [3:0]  efuse_val_csr_sds_pll_bias_sel_icc;
    logic [3:0]  efuse_val_csr_sds_ldorxslc_vsel;
    logic [3:0]  efuse_val_csr_sds_ldo_tx_vsel;
    logic [3:0]  efuse_val_csr_sds_ldo_rx_vsel;
    logic [3:0]  efuse_val_csr_sds_ldo_clk_vsel;
} param_struct_t;


// ============================================
// cygnetpluse_otp_distributor
// Auto-generated from signal list
// Combinational logic distributor
// ============================================

module cygnetpluse_otp_distributor (
    input  logic [532:0]  chip_param,

    // Output segments
    output logic [63:0]      uuid,
    output logic [15:0]      chip_id,
    output logic [3:0]      version_id,
    output logic [5:0]      bias_res_calib_e,
    output logic                   en_res_calib_e,
    output logic [3:0]      model_id_e,
    output logic [15:0]      temp_value_ref_e,
    output logic [12:0]      duty_cycle_ref_e,
    output logic [10:0]      one_over_k_e,
    output logic                   efuse_val_csr_cfg_xtal_div2_en,
    output logic                   efuse_val_csr_digpll_cfg_cp_current_from,
    output logic                   efuse_val_csr_digpll_cfg_r3,
    output logic                   efuse_val_csr_digpll_en_vco_bias_lpf,
    output logic                   efuse_val_csr_digpll_ensw_vco_core,
    output logic                   efuse_val_csr_digpll_ensw_vco_pre,
    output logic                   efuse_val_csr_digpll_inner_ldo_en,
    output logic                   efuse_val_csr_xtal_div2_en,
    output logic                   efuse_val_csr_xtal_div2_en_ana,
    output logic                   efuse_val_csr_xtal_ldo09_en,
    output logic                   efuse_val_csr_xtal_ldo26_en,
    output logic [1:0]      efuse_val_csr_digpll_cfg_bias_vco,
    output logic [1:0]      efuse_val_csr_digpll_cfg_c1,
    output logic [1:0]      efuse_val_csr_digpll_cfg_c2,
    output logic [1:0]      efuse_val_csr_digpll_cfg_ldo_vsel,
    output logic [1:0]      efuse_val_csr_digpll_cfg_r2,
    output logic [2:0]      efuse_val_csr_digpll_cfg_cp_current,
    output logic [2:0]      efuse_val_csr_digpll_cfg_vco_band,
    output logic [2:0]      efuse_val_csr_digpll_cfg_vco_up,
    output logic [2:0]      efuse_val_csr_xtal_ldo09_vsel,
    output logic [2:0]      efuse_val_csr_xtal_ldo26_vsel,
    output logic [3:0]      efuse_val_csr_digpll_bias_ext,
    output logic [3:0]      efuse_val_csr_digpll_bias_int,
    output logic                   efuse_val_csr_10g_sds_pll_band_en,
    output logic                   efuse_val_csr_12g_sds_pll_band_en,
    output logic [3:0]      efuse_val_csr_c16_ki_c2_cors,
    output logic [3:0]      efuse_val_csr_c16_ki_c2_fine,
    output logic [2:0]      efuse_val_csr_c16_ki_coe_cors,
    output logic [2:0]      efuse_val_csr_c16_ki_coe_fine,
    output logic [3:0]      efuse_val_csr_cdr_c1_c20,
    output logic [3:0]      efuse_val_csr_cdr_c1_c20_fine,
    output logic [3:0]      efuse_val_csr_cdr_c1_c32,
    output logic [3:0]      efuse_val_csr_cdr_c1_c32_fine,
    output logic [3:0]      efuse_val_csr_cdr_c2_c20,
    output logic [3:0]      efuse_val_csr_cdr_c2_c20_fine,
    output logic [3:0]      efuse_val_csr_cdr_c2_c32,
    output logic [3:0]      efuse_val_csr_cdr_c2_c32_fine,
    output logic [7:0]      efuse_val_csr_cdr_lock_tm_lpwr,
    output logic [8:0]      efuse_val_csr_csr_c16_kp_out,
    output logic                   efuse_val_csr_en_pcie_lp,
    output logic [6:0]      efuse_val_csr_eod_height_rect,
    output logic [6:0]      efuse_val_csr_eod_height_tri,
    output logic                   efuse_val_csr_eod_shape_tri_rect,
    output logic [5:0]      efuse_val_csr_eod_wth_rect,
    output logic [5:0]      efuse_val_csr_eod_wth_tri,
    output logic [3:0]      efuse_val_csr_sigdet_loss_to,
    output logic                   efuse_val_csr_man_sds_afe_ctle_peak_en,
    output logic                   efuse_val_csr_man_sds_afe_pga_gain_en,
    output logic [3:0]      efuse_val_csr_sds_pll_vcoldo_vtune,
    output logic [0:0]      efuse_val_csr_sds_pll_vcoldo_en_ext,
    output logic [0:0]      efuse_val_csr_sds_pll_vcoldo_en,
    output logic [3:0]      efuse_val_csr_sds_pll_vco_sel_vco2_current,
    output logic [5:0]      efuse_val_csr_sds_pll_vco_iptat,
    output logic [5:0]      efuse_val_csr_sds_pll_vco_iconstant,
    output logic [1:0]      efuse_val_csr_sds_pll_pllldo_vtune,
    output logic [0:0]      efuse_val_csr_sds_pll_pllldo_en_ext,
    output logic [0:0]      efuse_val_csr_sds_pll_pllldo_en,
    output logic [3:0]      efuse_val_csr_sds_pll_pdivn_s,
    output logic [9:0]      efuse_val_csr_sds_pll_pdivn_p,
    output logic [3:0]      efuse_val_csr_sds_pll_fdivn_s,
    output logic [9:0]      efuse_val_csr_sds_pll_fdivn_p,
    output logic [3:0]      efuse_val_csr_sds_pll_bias_sel_iptat,
    output logic [3:0]      efuse_val_csr_sds_pll_bias_sel_icc,
    output logic [3:0]      efuse_val_csr_sds_ldorxslc_vsel,
    output logic [3:0]      efuse_val_csr_sds_ldo_tx_vsel,
    output logic [3:0]      efuse_val_csr_sds_ldo_rx_vsel,
    output logic [3:0]      efuse_val_csr_sds_ldo_clk_vsel
);

    // Combinational logic distribution
    always_comb begin
        uuid = chip_param[63:0]; // value: 0x0
        chip_id = {~chip_param[79], chip_param[78], chip_param[77], ~chip_param[76], chip_param[75], chip_param[74], chip_param[73], chip_param[72], chip_param[71], chip_param[70], chip_param[69], chip_param[68], ~chip_param[67], chip_param[66], chip_param[65], chip_param[64]}; // value: 0x9008
        version_id = chip_param[83:80]; // value: 0x0
        bias_res_calib_e = {~chip_param[89], chip_param[88], chip_param[87], chip_param[86], chip_param[85], chip_param[84]}; // value: 0x20
        en_res_calib_e = chip_param[90]; // value: 0x0
        model_id_e = chip_param[94:91]; // value: 0x0
        temp_value_ref_e = chip_param[110:95]; // value: 0x0
        duty_cycle_ref_e = chip_param[123:111]; // value: 0x0
        one_over_k_e = chip_param[134:124]; // value: 0x0
        efuse_val_csr_cfg_xtal_div2_en = chip_param[135]; // value: 0x0
        efuse_val_csr_digpll_cfg_cp_current_from = chip_param[136]; // value: 0x0
        efuse_val_csr_digpll_cfg_r3 = chip_param[137]; // value: 0x0
        efuse_val_csr_digpll_en_vco_bias_lpf = ~chip_param[138]; // value: 0x1
        efuse_val_csr_digpll_ensw_vco_core = ~chip_param[139]; // value: 0x1
        efuse_val_csr_digpll_ensw_vco_pre = chip_param[140]; // value: 0x0
        efuse_val_csr_digpll_inner_ldo_en = ~chip_param[141]; // value: 0x1
        efuse_val_csr_xtal_div2_en = chip_param[142]; // value: 0x0
        efuse_val_csr_xtal_div2_en_ana = chip_param[143]; // value: 0x0
        efuse_val_csr_xtal_ldo09_en = chip_param[144]; // value: 0x0
        efuse_val_csr_xtal_ldo26_en = chip_param[145]; // value: 0x0
        efuse_val_csr_digpll_cfg_bias_vco = {~chip_param[147], chip_param[146]}; // value: 0x2
        efuse_val_csr_digpll_cfg_c1 = {~chip_param[149], chip_param[148]}; // value: 0x2
        efuse_val_csr_digpll_cfg_c2 = {~chip_param[151], ~chip_param[150]}; // value: 0x3
        efuse_val_csr_digpll_cfg_ldo_vsel = {chip_param[153], ~chip_param[152]}; // value: 0x1
        efuse_val_csr_digpll_cfg_r2 = {chip_param[155], ~chip_param[154]}; // value: 0x1
        efuse_val_csr_digpll_cfg_cp_current = {~chip_param[158], chip_param[157], chip_param[156]}; // value: 0x4
        efuse_val_csr_digpll_cfg_vco_band = {chip_param[161], ~chip_param[160], ~chip_param[159]}; // value: 0x3
        efuse_val_csr_digpll_cfg_vco_up = {~chip_param[164], chip_param[163], chip_param[162]}; // value: 0x4
        efuse_val_csr_xtal_ldo09_vsel = chip_param[167:165]; // value: 0x0
        efuse_val_csr_xtal_ldo26_vsel = chip_param[170:168]; // value: 0x0
        efuse_val_csr_digpll_bias_ext = {chip_param[174], ~chip_param[173], chip_param[172], ~chip_param[171]}; // value: 0x5
        efuse_val_csr_digpll_bias_int = {chip_param[178], ~chip_param[177], chip_param[176], ~chip_param[175]}; // value: 0x5
        efuse_val_csr_10g_sds_pll_band_en = chip_param[356]; // value: 0x0
        efuse_val_csr_12g_sds_pll_band_en = chip_param[357]; // value: 0x0
        efuse_val_csr_c16_ki_c2_cors = {chip_param[361], ~chip_param[360], ~chip_param[359], ~chip_param[358]}; // value: 0x7
        efuse_val_csr_c16_ki_c2_fine = {~chip_param[365], chip_param[364], chip_param[363], chip_param[362]}; // value: 0x8
        efuse_val_csr_c16_ki_coe_cors = chip_param[368:366]; // value: 0x0
        efuse_val_csr_c16_ki_coe_fine = chip_param[371:369]; // value: 0x0
        efuse_val_csr_cdr_c1_c20 = {chip_param[375], ~chip_param[374], chip_param[373], chip_param[372]}; // value: 0x4
        efuse_val_csr_cdr_c1_c20_fine = {chip_param[379], ~chip_param[378], chip_param[377], ~chip_param[376]}; // value: 0x5
        efuse_val_csr_cdr_c1_c32 = {chip_param[383], ~chip_param[382], chip_param[381], chip_param[380]}; // value: 0x4
        efuse_val_csr_cdr_c1_c32_fine = {chip_param[387], ~chip_param[386], chip_param[385], ~chip_param[384]}; // value: 0x5
        efuse_val_csr_cdr_c2_c20 = {chip_param[391], ~chip_param[390], ~chip_param[389], chip_param[388]}; // value: 0x6
        efuse_val_csr_cdr_c2_c20_fine = {~chip_param[395], chip_param[394], chip_param[393], chip_param[392]}; // value: 0x8
        efuse_val_csr_cdr_c2_c32 = {chip_param[399], ~chip_param[398], ~chip_param[397], chip_param[396]}; // value: 0x6
        efuse_val_csr_cdr_c2_c32_fine = {~chip_param[403], chip_param[402], chip_param[401], chip_param[400]}; // value: 0x8
        efuse_val_csr_cdr_lock_tm_lpwr = chip_param[411:404]; // value: 0x0
        efuse_val_csr_csr_c16_kp_out = {chip_param[420], chip_param[419], chip_param[418], chip_param[417], chip_param[416], ~chip_param[415], chip_param[414], chip_param[413], ~chip_param[412]}; // value: 0x9
        efuse_val_csr_en_pcie_lp = chip_param[421]; // value: 0x0
        efuse_val_csr_eod_height_rect = {chip_param[428], chip_param[427], chip_param[426], ~chip_param[425], ~chip_param[424], ~chip_param[423], ~chip_param[422]}; // value: 0xf
        efuse_val_csr_eod_height_tri = {chip_param[435], chip_param[434], chip_param[433], ~chip_param[432], ~chip_param[431], ~chip_param[430], ~chip_param[429]}; // value: 0xf
        efuse_val_csr_eod_shape_tri_rect = chip_param[436]; // value: 0x0
        efuse_val_csr_eod_wth_rect = {chip_param[442], chip_param[441], chip_param[440], ~chip_param[439], chip_param[438], ~chip_param[437]}; // value: 0x5
        efuse_val_csr_eod_wth_tri = {chip_param[448], chip_param[447], chip_param[446], ~chip_param[445], chip_param[444], ~chip_param[443]}; // value: 0x5
        efuse_val_csr_sigdet_loss_to = chip_param[452:449]; // value: 0x0
        efuse_val_csr_man_sds_afe_ctle_peak_en = chip_param[453]; // value: 0x0
        efuse_val_csr_man_sds_afe_pga_gain_en = chip_param[454]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_vtune = {~chip_param[458], chip_param[457], chip_param[456], chip_param[455]}; // value: 0x8
        efuse_val_csr_sds_pll_vcoldo_en_ext = chip_param[459]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_en = ~chip_param[460]; // value: 0x1
        efuse_val_csr_sds_pll_vco_sel_vco2_current = {~chip_param[464], chip_param[463], chip_param[462], ~chip_param[461]}; // value: 0x9
        efuse_val_csr_sds_pll_vco_iptat = {chip_param[470], ~chip_param[469], ~chip_param[468], chip_param[467], chip_param[466], chip_param[465]}; // value: 0x18
        efuse_val_csr_sds_pll_vco_iconstant = {chip_param[476], ~chip_param[475], chip_param[474], ~chip_param[473], ~chip_param[472], chip_param[471]}; // value: 0x16
        efuse_val_csr_sds_pll_pllldo_vtune = {chip_param[478], ~chip_param[477]}; // value: 0x1
        efuse_val_csr_sds_pll_pllldo_en_ext = chip_param[479]; // value: 0x0
        efuse_val_csr_sds_pll_pllldo_en = ~chip_param[480]; // value: 0x1
        efuse_val_csr_sds_pll_pdivn_s = {chip_param[484], chip_param[483], ~chip_param[482], chip_param[481]}; // value: 0x2
        efuse_val_csr_sds_pll_pdivn_p = {chip_param[494], chip_param[493], chip_param[492], chip_param[491], ~chip_param[490], ~chip_param[489], ~chip_param[488], ~chip_param[487], ~chip_param[486], chip_param[485]}; // value: 0x3E
        efuse_val_csr_sds_pll_fdivn_s = {chip_param[498], chip_param[497], chip_param[496], ~chip_param[495]}; // value: 0x1
        efuse_val_csr_sds_pll_fdivn_p = {chip_param[508], chip_param[507], chip_param[506], chip_param[505], ~chip_param[504], chip_param[503], ~chip_param[502], chip_param[501], chip_param[500], ~chip_param[499]}; // value: 0x29
        efuse_val_csr_sds_pll_bias_sel_iptat = {chip_param[512], chip_param[511], ~chip_param[510], chip_param[509]}; // value: 0x2
        efuse_val_csr_sds_pll_bias_sel_icc = {chip_param[516], chip_param[515], ~chip_param[514], chip_param[513]}; // value: 0x2
        efuse_val_csr_sds_ldorxslc_vsel = {chip_param[520], ~chip_param[519], chip_param[518], chip_param[517]}; // value: 0x4
        efuse_val_csr_sds_ldo_tx_vsel = {chip_param[524], ~chip_param[523], chip_param[522], chip_param[521]}; // value: 0x4
        efuse_val_csr_sds_ldo_rx_vsel = {chip_param[528], ~chip_param[527], chip_param[526], chip_param[525]}; // value: 0x4
        efuse_val_csr_sds_ldo_clk_vsel = {chip_param[532], ~chip_param[531], chip_param[530], chip_param[529]}; // value: 0x4
    end

endmodule

