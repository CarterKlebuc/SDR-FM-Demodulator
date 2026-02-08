# GNU Radio SDR FM Demodulator README

# Summary

This project is an FM Demodulator built in GNU Radio for the RTL-SDR v4. The project’s purpose is to learn how to use GNURadio and implement DSP concepts for a Software Defined Radio application.

# Flowgraph

![Screenshot 2025-01-19 120846](https://github.com/CarterKlebuc/SDR-FM-Demodulator/blob/5f4bed3fd1f6ed0dc270aa8a6386624b96862e9d/FlowgraphImage.png)

The RTL-SDR source is fed into a Low Pass Decimation filter to convert the sampling rate from 2.4 [MHz] to 240 [kHz]. After FM demodulation, the demodulated signal is fed into another Low Pass Decimation filter to convert the sampling rate from 240 [kHz] to 48 [kHz] for proper audio output. The audio output is fed through an FM De-emphasis filter and then output.

# UI

![Screenshot 2025-01-19 120846](https://github.com/CarterKlebuc/SDR-FM-Demodulator/blob/5f4bed3fd1f6ed0dc270aa8a6386624b96862e9d/Frontend%20SDR%20UI.png)

The UI was designed in QtDesigner and then manually integrated with the GNU Radio Python script. The waterfall plot was added to indicate the strong reception of FM radio stations to the user. The user can manually adjust the center frequency and RF gain via the sliders. The user can pause and restart radio reception via the top button.

# How to use

1.  Create a Python virtual environment that has access to GNU Radio.
2.  Ensure PyQt5 is installed on your system.
3.  Run [main.py](http://main.py)

# Resources

-   [https://wiki.gnuradio.org/index.php?title=GNU_Radio_Flowgraph_Embedded_in_Python_Applications](https://wiki.gnuradio.org/index.php?title=GNU_Radio_Flowgraph_Embedded_in_Python_Applications)
-   Book: Software Defined Radio Using MATLAB & Simulink and the RTL-SDR
-   -   Link: [https://www.mathworks.com/campaigns/offers/download-rtl-sdr-ebook.html](https://www.mathworks.com/campaigns/offers/download-rtl-sdr-ebook.html)
