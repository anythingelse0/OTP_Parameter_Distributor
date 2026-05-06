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
    logic [8:0]  efuse_val_csr_10g_sds_pll_band_w;
    logic              efuse_val_csr_12g_sds_pll_band_en;
    logic [8:0]  efuse_val_csr_12g_sds_pll_band_w;
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
    logic [3:0]  efuse_val_csr_sds_afe_ctle_peak_w;
    logic [2:0]  efuse_val_csr_sds_afe_pga_gain_w;
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
    logic              efuse_val_csr_10g_sds_pll_band_en_1;
    logic [8:0]  efuse_val_csr_10g_sds_pll_band_w_1;
    logic              efuse_val_csr_12g_sds_pll_band_en_1;
    logic [8:0]  efuse_val_csr_12g_sds_pll_band_w_1;
    logic [3:0]  efuse_val_csr_c16_ki_c2_cors_1;
    logic [3:0]  efuse_val_csr_c16_ki_c2_fine_1;
    logic [2:0]  efuse_val_csr_c16_ki_coe_cors_1;
    logic [2:0]  efuse_val_csr_c16_ki_coe_fine_1;
    logic [3:0]  efuse_val_csr_cdr_c1_c20_1;
    logic [3:0]  efuse_val_csr_cdr_c1_c20_fine_1;
    logic [3:0]  efuse_val_csr_cdr_c1_c32_1;
    logic [3:0]  efuse_val_csr_cdr_c1_c32_fine_1;
    logic [3:0]  efuse_val_csr_cdr_c2_c20_1;
    logic [3:0]  efuse_val_csr_cdr_c2_c20_fine_1;
    logic [3:0]  efuse_val_csr_cdr_c2_c32_1;
    logic [3:0]  efuse_val_csr_cdr_c2_c32_fine_1;
    logic [7:0]  efuse_val_csr_cdr_lock_tm_lpwr_1;
    logic [8:0]  efuse_val_csr_csr_c16_kp_out_1;
    logic              efuse_val_csr_en_pcie_lp_1;
    logic [6:0]  efuse_val_csr_eod_height_rect_1;
    logic [6:0]  efuse_val_csr_eod_height_tri_1;
    logic              efuse_val_csr_eod_shape_tri_rect_1;
    logic [5:0]  efuse_val_csr_eod_wth_rect_1;
    logic [5:0]  efuse_val_csr_eod_wth_tri_1;
    logic [3:0]  efuse_val_csr_sigdet_loss_to_1;
    logic              efuse_val_csr_man_sds_afe_ctle_peak_en_1;
    logic              efuse_val_csr_man_sds_afe_pga_gain_en_1;
    logic [3:0]  efuse_val_csr_sds_afe_ctle_peak_w_1;
    logic [2:0]  efuse_val_csr_sds_afe_pga_gain_w_1;
    logic [3:0]  efuse_val_csr_sds_pll_vcoldo_vtune_1;
    logic              efuse_val_csr_sds_pll_vcoldo_en_ext_1;
    logic              efuse_val_csr_sds_pll_vcoldo_en_1;
    logic [3:0]  efuse_val_csr_sds_pll_vco_sel_vco2_current_1;
    logic [5:0]  efuse_val_csr_sds_pll_vco_iptat_1;
    logic [5:0]  efuse_val_csr_sds_pll_vco_iconstant_1;
    logic [1:0]  efuse_val_csr_sds_pll_pllldo_vtune_1;
    logic              efuse_val_csr_sds_pll_pllldo_en_ext_1;
    logic              efuse_val_csr_sds_pll_pllldo_en_1;
    logic [3:0]  efuse_val_csr_sds_pll_pdivn_s_1;
    logic [9:0]  efuse_val_csr_sds_pll_pdivn_p_1;
    logic [3:0]  efuse_val_csr_sds_pll_fdivn_s_1;
    logic [9:0]  efuse_val_csr_sds_pll_fdivn_p_1;
    logic [3:0]  efuse_val_csr_sds_pll_bias_sel_iptat_1;
    logic [3:0]  efuse_val_csr_sds_pll_bias_sel_icc_1;
    logic [3:0]  efuse_val_csr_sds_ldorxslc_vsel_1;
    logic [3:0]  efuse_val_csr_sds_ldo_tx_vsel_1;
    logic [3:0]  efuse_val_csr_sds_ldo_rx_vsel_1;
    logic [3:0]  efuse_val_csr_sds_ldo_clk_vsel_1;
} param_struct_t;


module cygnetpluse_otp_distributor (
    input  logic [582:0]  chip_param,

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
    output logic [8:0]      efuse_val_csr_10g_sds_pll_band_w,
    output logic                   efuse_val_csr_12g_sds_pll_band_en,
    output logic [8:0]      efuse_val_csr_12g_sds_pll_band_w,
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
    output logic [3:0]      efuse_val_csr_sds_afe_ctle_peak_w,
    output logic [2:0]      efuse_val_csr_sds_afe_pga_gain_w,
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
    output logic [3:0]      efuse_val_csr_sds_ldo_clk_vsel,
    output logic                   efuse_val_csr_10g_sds_pll_band_en_1,
    output logic [8:0]      efuse_val_csr_10g_sds_pll_band_w_1,
    output logic                   efuse_val_csr_12g_sds_pll_band_en_1,
    output logic [8:0]      efuse_val_csr_12g_sds_pll_band_w_1,
    output logic [3:0]      efuse_val_csr_c16_ki_c2_cors_1,
    output logic [3:0]      efuse_val_csr_c16_ki_c2_fine_1,
    output logic [2:0]      efuse_val_csr_c16_ki_coe_cors_1,
    output logic [2:0]      efuse_val_csr_c16_ki_coe_fine_1,
    output logic [3:0]      efuse_val_csr_cdr_c1_c20_1,
    output logic [3:0]      efuse_val_csr_cdr_c1_c20_fine_1,
    output logic [3:0]      efuse_val_csr_cdr_c1_c32_1,
    output logic [3:0]      efuse_val_csr_cdr_c1_c32_fine_1,
    output logic [3:0]      efuse_val_csr_cdr_c2_c20_1,
    output logic [3:0]      efuse_val_csr_cdr_c2_c20_fine_1,
    output logic [3:0]      efuse_val_csr_cdr_c2_c32_1,
    output logic [3:0]      efuse_val_csr_cdr_c2_c32_fine_1,
    output logic [7:0]      efuse_val_csr_cdr_lock_tm_lpwr_1,
    output logic [8:0]      efuse_val_csr_csr_c16_kp_out_1,
    output logic                   efuse_val_csr_en_pcie_lp_1,
    output logic [6:0]      efuse_val_csr_eod_height_rect_1,
    output logic [6:0]      efuse_val_csr_eod_height_tri_1,
    output logic                   efuse_val_csr_eod_shape_tri_rect_1,
    output logic [5:0]      efuse_val_csr_eod_wth_rect_1,
    output logic [5:0]      efuse_val_csr_eod_wth_tri_1,
    output logic [3:0]      efuse_val_csr_sigdet_loss_to_1,
    output logic                   efuse_val_csr_man_sds_afe_ctle_peak_en_1,
    output logic                   efuse_val_csr_man_sds_afe_pga_gain_en_1,
    output logic [3:0]      efuse_val_csr_sds_afe_ctle_peak_w_1,
    output logic [2:0]      efuse_val_csr_sds_afe_pga_gain_w_1,
    output logic [3:0]      efuse_val_csr_sds_pll_vcoldo_vtune_1,
    output logic [0:0]      efuse_val_csr_sds_pll_vcoldo_en_ext_1,
    output logic [0:0]      efuse_val_csr_sds_pll_vcoldo_en_1,
    output logic [3:0]      efuse_val_csr_sds_pll_vco_sel_vco2_current_1,
    output logic [5:0]      efuse_val_csr_sds_pll_vco_iptat_1,
    output logic [5:0]      efuse_val_csr_sds_pll_vco_iconstant_1,
    output logic [1:0]      efuse_val_csr_sds_pll_pllldo_vtune_1,
    output logic [0:0]      efuse_val_csr_sds_pll_pllldo_en_ext_1,
    output logic [0:0]      efuse_val_csr_sds_pll_pllldo_en_1,
    output logic [3:0]      efuse_val_csr_sds_pll_pdivn_s_1,
    output logic [9:0]      efuse_val_csr_sds_pll_pdivn_p_1,
    output logic [3:0]      efuse_val_csr_sds_pll_fdivn_s_1,
    output logic [9:0]      efuse_val_csr_sds_pll_fdivn_p_1,
    output logic [3:0]      efuse_val_csr_sds_pll_bias_sel_iptat_1,
    output logic [3:0]      efuse_val_csr_sds_pll_bias_sel_icc_1,
    output logic [3:0]      efuse_val_csr_sds_ldorxslc_vsel_1,
    output logic [3:0]      efuse_val_csr_sds_ldo_tx_vsel_1,
    output logic [3:0]      efuse_val_csr_sds_ldo_rx_vsel_1,
    output logic [3:0]      efuse_val_csr_sds_ldo_clk_vsel_1
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
        efuse_val_csr_10g_sds_pll_band_en = chip_param[179]; // value: 0x0
        efuse_val_csr_10g_sds_pll_band_w = chip_param[188:180]; // value: 0x0
        efuse_val_csr_12g_sds_pll_band_en = chip_param[189]; // value: 0x0
        efuse_val_csr_12g_sds_pll_band_w = chip_param[198:190]; // value: 0x0
        efuse_val_csr_c16_ki_c2_cors = {chip_param[202], ~chip_param[201], ~chip_param[200], ~chip_param[199]}; // value: 0x7
        efuse_val_csr_c16_ki_c2_fine = {~chip_param[206], chip_param[205], chip_param[204], chip_param[203]}; // value: 0x8
        efuse_val_csr_c16_ki_coe_cors = chip_param[209:207]; // value: 0x0
        efuse_val_csr_c16_ki_coe_fine = chip_param[212:210]; // value: 0x0
        efuse_val_csr_cdr_c1_c20 = {chip_param[216], ~chip_param[215], chip_param[214], chip_param[213]}; // value: 0x4
        efuse_val_csr_cdr_c1_c20_fine = {chip_param[220], ~chip_param[219], chip_param[218], ~chip_param[217]}; // value: 0x5
        efuse_val_csr_cdr_c1_c32 = {chip_param[224], ~chip_param[223], chip_param[222], chip_param[221]}; // value: 0x4
        efuse_val_csr_cdr_c1_c32_fine = {chip_param[228], ~chip_param[227], chip_param[226], ~chip_param[225]}; // value: 0x5
        efuse_val_csr_cdr_c2_c20 = {chip_param[232], ~chip_param[231], ~chip_param[230], chip_param[229]}; // value: 0x6
        efuse_val_csr_cdr_c2_c20_fine = {~chip_param[236], chip_param[235], chip_param[234], chip_param[233]}; // value: 0x8
        efuse_val_csr_cdr_c2_c32 = {chip_param[240], ~chip_param[239], ~chip_param[238], chip_param[237]}; // value: 0x6
        efuse_val_csr_cdr_c2_c32_fine = {~chip_param[244], chip_param[243], chip_param[242], chip_param[241]}; // value: 0x8
        efuse_val_csr_cdr_lock_tm_lpwr = chip_param[252:245]; // value: 0x0
        efuse_val_csr_csr_c16_kp_out = {chip_param[261], chip_param[260], chip_param[259], chip_param[258], chip_param[257], ~chip_param[256], chip_param[255], chip_param[254], ~chip_param[253]}; // value: 0x9
        efuse_val_csr_en_pcie_lp = chip_param[262]; // value: 0x0
        efuse_val_csr_eod_height_rect = {chip_param[269], chip_param[268], chip_param[267], ~chip_param[266], ~chip_param[265], ~chip_param[264], ~chip_param[263]}; // value: 0xf
        efuse_val_csr_eod_height_tri = {chip_param[276], chip_param[275], chip_param[274], ~chip_param[273], ~chip_param[272], ~chip_param[271], ~chip_param[270]}; // value: 0xf
        efuse_val_csr_eod_shape_tri_rect = chip_param[277]; // value: 0x0
        efuse_val_csr_eod_wth_rect = {chip_param[283], chip_param[282], chip_param[281], ~chip_param[280], chip_param[279], ~chip_param[278]}; // value: 0x5
        efuse_val_csr_eod_wth_tri = {chip_param[289], chip_param[288], chip_param[287], ~chip_param[286], chip_param[285], ~chip_param[284]}; // value: 0x5
        efuse_val_csr_sigdet_loss_to = chip_param[293:290]; // value: 0x0
        efuse_val_csr_man_sds_afe_ctle_peak_en = chip_param[294]; // value: 0x0
        efuse_val_csr_man_sds_afe_pga_gain_en = chip_param[295]; // value: 0x0
        efuse_val_csr_sds_afe_ctle_peak_w = chip_param[299:296]; // value: 0x0
        efuse_val_csr_sds_afe_pga_gain_w = chip_param[302:300]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_vtune = {~chip_param[306], chip_param[305], chip_param[304], chip_param[303]}; // value: 0x8
        efuse_val_csr_sds_pll_vcoldo_en_ext = chip_param[307]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_en = ~chip_param[308]; // value: 0x1
        efuse_val_csr_sds_pll_vco_sel_vco2_current = {~chip_param[312], chip_param[311], chip_param[310], ~chip_param[309]}; // value: 0x9
        efuse_val_csr_sds_pll_vco_iptat = {chip_param[318], ~chip_param[317], ~chip_param[316], chip_param[315], chip_param[314], chip_param[313]}; // value: 0x18
        efuse_val_csr_sds_pll_vco_iconstant = {chip_param[324], ~chip_param[323], chip_param[322], ~chip_param[321], ~chip_param[320], chip_param[319]}; // value: 0x16
        efuse_val_csr_sds_pll_pllldo_vtune = {chip_param[326], ~chip_param[325]}; // value: 0x1
        efuse_val_csr_sds_pll_pllldo_en_ext = chip_param[327]; // value: 0x0
        efuse_val_csr_sds_pll_pllldo_en = ~chip_param[328]; // value: 0x1
        efuse_val_csr_sds_pll_pdivn_s = {chip_param[332], chip_param[331], ~chip_param[330], chip_param[329]}; // value: 0x2
        efuse_val_csr_sds_pll_pdivn_p = {chip_param[342], chip_param[341], chip_param[340], chip_param[339], ~chip_param[338], ~chip_param[337], ~chip_param[336], ~chip_param[335], ~chip_param[334], chip_param[333]}; // value: 0x3E
        efuse_val_csr_sds_pll_fdivn_s = {chip_param[346], chip_param[345], chip_param[344], ~chip_param[343]}; // value: 0x1
        efuse_val_csr_sds_pll_fdivn_p = {chip_param[356], chip_param[355], chip_param[354], chip_param[353], ~chip_param[352], chip_param[351], ~chip_param[350], chip_param[349], chip_param[348], ~chip_param[347]}; // value: 0x29
        efuse_val_csr_sds_pll_bias_sel_iptat = {chip_param[360], chip_param[359], ~chip_param[358], chip_param[357]}; // value: 0x2
        efuse_val_csr_sds_pll_bias_sel_icc = {chip_param[364], chip_param[363], ~chip_param[362], chip_param[361]}; // value: 0x2
        efuse_val_csr_sds_ldorxslc_vsel = {chip_param[368], ~chip_param[367], chip_param[366], chip_param[365]}; // value: 0x4
        efuse_val_csr_sds_ldo_tx_vsel = {chip_param[372], ~chip_param[371], chip_param[370], chip_param[369]}; // value: 0x4
        efuse_val_csr_sds_ldo_rx_vsel = {chip_param[376], ~chip_param[375], chip_param[374], chip_param[373]}; // value: 0x4
        efuse_val_csr_sds_ldo_clk_vsel = {chip_param[380], ~chip_param[379], chip_param[378], chip_param[377]}; // value: 0x4
        efuse_val_csr_10g_sds_pll_band_en_1 = chip_param[381]; // value: 0x0
        efuse_val_csr_10g_sds_pll_band_w_1 = chip_param[390:382]; // value: 0x0
        efuse_val_csr_12g_sds_pll_band_en_1 = chip_param[391]; // value: 0x0
        efuse_val_csr_12g_sds_pll_band_w_1 = chip_param[400:392]; // value: 0x0
        efuse_val_csr_c16_ki_c2_cors_1 = {chip_param[404], ~chip_param[403], ~chip_param[402], ~chip_param[401]}; // value: 0x7
        efuse_val_csr_c16_ki_c2_fine_1 = {~chip_param[408], chip_param[407], chip_param[406], chip_param[405]}; // value: 0x8
        efuse_val_csr_c16_ki_coe_cors_1 = chip_param[411:409]; // value: 0x0
        efuse_val_csr_c16_ki_coe_fine_1 = chip_param[414:412]; // value: 0x0
        efuse_val_csr_cdr_c1_c20_1 = {chip_param[418], ~chip_param[417], chip_param[416], chip_param[415]}; // value: 0x4
        efuse_val_csr_cdr_c1_c20_fine_1 = {chip_param[422], ~chip_param[421], chip_param[420], ~chip_param[419]}; // value: 0x5
        efuse_val_csr_cdr_c1_c32_1 = {chip_param[426], ~chip_param[425], chip_param[424], chip_param[423]}; // value: 0x4
        efuse_val_csr_cdr_c1_c32_fine_1 = {chip_param[430], ~chip_param[429], chip_param[428], ~chip_param[427]}; // value: 0x5
        efuse_val_csr_cdr_c2_c20_1 = {chip_param[434], ~chip_param[433], ~chip_param[432], chip_param[431]}; // value: 0x6
        efuse_val_csr_cdr_c2_c20_fine_1 = {~chip_param[438], chip_param[437], chip_param[436], chip_param[435]}; // value: 0x8
        efuse_val_csr_cdr_c2_c32_1 = {chip_param[442], ~chip_param[441], ~chip_param[440], chip_param[439]}; // value: 0x6
        efuse_val_csr_cdr_c2_c32_fine_1 = {~chip_param[446], chip_param[445], chip_param[444], chip_param[443]}; // value: 0x8
        efuse_val_csr_cdr_lock_tm_lpwr_1 = chip_param[454:447]; // value: 0x0
        efuse_val_csr_csr_c16_kp_out_1 = {chip_param[463], chip_param[462], chip_param[461], chip_param[460], chip_param[459], ~chip_param[458], chip_param[457], chip_param[456], ~chip_param[455]}; // value: 0x9
        efuse_val_csr_en_pcie_lp_1 = chip_param[464]; // value: 0x0
        efuse_val_csr_eod_height_rect_1 = {chip_param[471], chip_param[470], chip_param[469], ~chip_param[468], ~chip_param[467], ~chip_param[466], ~chip_param[465]}; // value: 0xf
        efuse_val_csr_eod_height_tri_1 = {chip_param[478], chip_param[477], chip_param[476], ~chip_param[475], ~chip_param[474], ~chip_param[473], ~chip_param[472]}; // value: 0xf
        efuse_val_csr_eod_shape_tri_rect_1 = chip_param[479]; // value: 0x0
        efuse_val_csr_eod_wth_rect_1 = {chip_param[485], chip_param[484], chip_param[483], ~chip_param[482], chip_param[481], ~chip_param[480]}; // value: 0x5
        efuse_val_csr_eod_wth_tri_1 = {chip_param[491], chip_param[490], chip_param[489], ~chip_param[488], chip_param[487], ~chip_param[486]}; // value: 0x5
        efuse_val_csr_sigdet_loss_to_1 = chip_param[495:492]; // value: 0x0
        efuse_val_csr_man_sds_afe_ctle_peak_en_1 = chip_param[496]; // value: 0x0
        efuse_val_csr_man_sds_afe_pga_gain_en_1 = chip_param[497]; // value: 0x0
        efuse_val_csr_sds_afe_ctle_peak_w_1 = chip_param[501:498]; // value: 0x0
        efuse_val_csr_sds_afe_pga_gain_w_1 = chip_param[504:502]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_vtune_1 = {~chip_param[508], chip_param[507], chip_param[506], chip_param[505]}; // value: 0x8
        efuse_val_csr_sds_pll_vcoldo_en_ext_1 = chip_param[509]; // value: 0x0
        efuse_val_csr_sds_pll_vcoldo_en_1 = ~chip_param[510]; // value: 0x1
        efuse_val_csr_sds_pll_vco_sel_vco2_current_1 = {~chip_param[514], chip_param[513], chip_param[512], ~chip_param[511]}; // value: 0x9
        efuse_val_csr_sds_pll_vco_iptat_1 = {chip_param[520], ~chip_param[519], ~chip_param[518], chip_param[517], chip_param[516], chip_param[515]}; // value: 0x18
        efuse_val_csr_sds_pll_vco_iconstant_1 = {chip_param[526], ~chip_param[525], chip_param[524], ~chip_param[523], ~chip_param[522], chip_param[521]}; // value: 0x16
        efuse_val_csr_sds_pll_pllldo_vtune_1 = {chip_param[528], ~chip_param[527]}; // value: 0x1
        efuse_val_csr_sds_pll_pllldo_en_ext_1 = chip_param[529]; // value: 0x0
        efuse_val_csr_sds_pll_pllldo_en_1 = ~chip_param[530]; // value: 0x1
        efuse_val_csr_sds_pll_pdivn_s_1 = {chip_param[534], chip_param[533], ~chip_param[532], chip_param[531]}; // value: 0x2
        efuse_val_csr_sds_pll_pdivn_p_1 = {chip_param[544], chip_param[543], chip_param[542], chip_param[541], ~chip_param[540], ~chip_param[539], ~chip_param[538], ~chip_param[537], ~chip_param[536], chip_param[535]}; // value: 0x3E
        efuse_val_csr_sds_pll_fdivn_s_1 = {chip_param[548], chip_param[547], chip_param[546], ~chip_param[545]}; // value: 0x1
        efuse_val_csr_sds_pll_fdivn_p_1 = {chip_param[558], chip_param[557], chip_param[556], chip_param[555], ~chip_param[554], chip_param[553], ~chip_param[552], chip_param[551], chip_param[550], ~chip_param[549]}; // value: 0x29
        efuse_val_csr_sds_pll_bias_sel_iptat_1 = {chip_param[562], chip_param[561], ~chip_param[560], chip_param[559]}; // value: 0x2
        efuse_val_csr_sds_pll_bias_sel_icc_1 = {chip_param[566], chip_param[565], ~chip_param[564], chip_param[563]}; // value: 0x2
        efuse_val_csr_sds_ldorxslc_vsel_1 = {chip_param[570], ~chip_param[569], chip_param[568], chip_param[567]}; // value: 0x4
        efuse_val_csr_sds_ldo_tx_vsel_1 = {chip_param[574], ~chip_param[573], chip_param[572], chip_param[571]}; // value: 0x4
        efuse_val_csr_sds_ldo_rx_vsel_1 = {chip_param[578], ~chip_param[577], chip_param[576], chip_param[575]}; // value: 0x4
        efuse_val_csr_sds_ldo_clk_vsel_1 = {chip_param[582], ~chip_param[581], chip_param[580], chip_param[579]}; // value: 0x4
    end

endmodule

