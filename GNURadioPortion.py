#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Hello
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip
import threading



class CarterCustomFMDemodSimulinkPort(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Hello", catch_exceptions=True)

        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.4e6
        self.center_frequency = center_frequency = 97.9e6
        self.rf_gain = 30

        ##################################################
        # Blocks
        ##################################################

        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(self.rf_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_frequency, #fc
            (samp_rate), #bw
            "Waterfall", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)


        self.low_pass_filter_1_0_0 = filter.fir_filter_fff(
            5,
            firdes.low_pass(
                1,
                (samp_rate / 10),
                21e3,
                3e3,
                window.WIN_BLACKMAN,
                6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_ccf(
            10,
            firdes.low_pass(
                1,
                (samp_rate * 2),
                90e3,
                30e3,
                window.WIN_BLACKMAN,
                6.76))
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff((samp_rate/10)/(2 * 3.14 * 75e3), 1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_conjugate_cc_0_0 = blocks.conjugate_cc()
        self.blocks_complex_to_magphase_1_0 = blocks.complex_to_magphase(1)
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=(samp_rate / (10 * 5)), tau=(75e-6))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_1_0, 1), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_complex_to_magphase_1_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_conjugate_cc_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_conjugate_cc_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.low_pass_filter_1_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_magphase_1_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.low_pass_filter_1_0_0, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "CarterCustomFMDemodSimulinkPort")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_multiply_const_xx_0.set_k((self.samp_rate/10)/(2 * 3.14 * 75e3))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, (self.samp_rate * 2), 90e3, 30e3, window.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_1_0_0.set_taps(firdes.low_pass(1, (self.samp_rate / 10), 21e3, 3e3, window.WIN_BLACKMAN, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, (self.samp_rate / 10))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, (self.samp_rate / 10))
        self.rtlsdr_source_0.set_center_freq(self.center_frequency, 0)

    def set_rf_gain(self, new_rf_gain):
        self.rf_gain = new_rf_gain
        self.rtlsdr_source_0.set_gain(self.rf_gain, 0)


def main(top_block_cls=CarterCustomFMDemodSimulinkPort, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
