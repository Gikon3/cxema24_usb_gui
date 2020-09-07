class ParserData:
    def __init__(self):
        self.data_frame = {}
        self.MAX_AMPL = 250
        self.MIN_AMPL = 10
        self.MODE_GPS = "GPS"
        self.MODE_GLO = "GLO"

    def parse_msg(self, msg, mode):
        import numpy as np
        for frame in msg:
            msg_split = []
            for cell in frame.split('.'):
                msg_split.append(cell.split(':'))
            # print(msg_split)
            g2 = int(msg_split.pop(0)[1])

            if g2 not in self.data_frame.keys():
                self.data_frame[g2] = np.array(msg_split, dtype=int)
            else:
                msg_split = np.array(msg_split, dtype=int)
                len_dataframe = len(self.data_frame[g2].ravel())
                if mode == self.MODE_GPS:
                    self.data_frame[g2] = np.append(self.data_frame[g2], msg_split).reshape((len_dataframe + 2) // 2, 2)
                else:
                    self.data_frame[g2] = np.append(self.data_frame[g2], msg_split).reshape((len_dataframe + 4) // 4, 2, 2)

    def get_g2_list(self):
        return self.data_frame.keys()

    def get_data_frame(self, g2):
        return self.data_frame[g2]

    def get_freq_list(self, g2, mode):
        import numpy as np
        ar_freq = np.array([])
        if mode == self.MODE_GPS:
            for freq, ampl in self.get_data_frame(g2):
                ar_freq = np.append(ar_freq, str(freq))
        else:
            for frame in self.get_data_frame(g2):
                for freq, ampl in frame:
                    ar_freq = np.append(ar_freq, str(freq))
        return ar_freq

    def get_ampl_list(self, g2, mode):
        import numpy as np
        ar_ampl = np.array([])
        if mode == self.MODE_GPS:
            for freq, ampl in self.get_data_frame(g2):
                ar_ampl = np.append(ar_ampl, ampl)
        else:
            for frame in self.get_data_frame(g2):
                for freq, ampl in frame:
                    ar_ampl = np.append(ar_ampl, ampl)
        return ar_ampl

    def get_numb_g2(self):
        return sum([1 for g2 in self.get_g2_list()])

    def get_max_ampl(self, mode):
        max_ampl = 0
        for g2 in self.get_g2_list():
            max_g2_ampl = max(self.get_ampl_list(g2, mode))
            if max_g2_ampl > max_ampl:
                max_ampl = max_g2_ampl
        return max_ampl

    def get_color_rgb(self, value):
        if value > self.MAX_AMPL:
            return 0, 1, 0
        elif value < self.MIN_AMPL:
            return 1, 0, 0
        ampl_range = self.MAX_AMPL - self.MIN_AMPL
        color_range = 1.0
        color_value = round((value - self.MIN_AMPL) * color_range / ampl_range, 8)
        return round(color_range - color_value, 8), color_value, 0

    def get_color_bar(self, ampl_list):
        color_list = []
        for ampl in ampl_list:
            color_list.append(self.get_color_rgb(ampl))
        return color_list

    def get_plot_pos(self):
        numb_fig = [1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 30, 36, 42]
        grid_fig = [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4),
                    (5, 4), (6, 4), (6, 5), (6, 6), (7, 6)]
        numb = self.get_numb_g2()
        count = 0
        while numb > numb_fig[count]:
            count += 1
        return grid_fig[count]

    def paint_window(self, mode='GPS'):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        import numpy as np
        x_range, y_range = self.get_plot_pos()
        fig = plt.figure(figsize=(16, 9), tight_layout=True)
        gs = fig.add_gridspec(x_range, y_range, )
        fig.suptitle("Amplitude distribution")
        max_ampl = self.get_max_ampl(mode)
        axs = []
        for count_ax in range(self.get_numb_g2()):
            x = int(count_ax % y_range)
            y = int(count_ax / y_range)
            # print(x_range, y_range, count_ax, x, y)
            g2 = list(self.get_g2_list())[count_ax]
            freq_list = self.get_freq_list(g2, mode)
            ampl_list = self.get_ampl_list(g2, mode)
            color_list = self.get_color_bar(self.get_ampl_list(g2, mode))
            # print(freq_list)
            # print(ampl_list)
            # print(color_list)
            axs.append(fig.add_subplot(gs[y, x]))
            x = np.arange(len(freq_list))
            axs[count_ax].bar(x, ampl_list, color=color_list)
            axs[count_ax].set_title(f"G:{g2}" if mode == "GPS" else f"Lit:{g2}", fontsize=10)
            axs[count_ax].set_xticks(x)
            axs[count_ax].set_xticklabels(freq_list)
            # axs[count_ax].set_xlabel("carrier frequency")
            # axs[count_ax].set_ylabel("amplitude")
            axs[count_ax].autoscale(True)
            axs[count_ax].grid(which='major',
                               axis='y')
            axs[count_ax].grid(which='minor',
                               axis='y',
                               linestyle='--')
            minor_step = 20
            axs[count_ax].yaxis.set_major_locator(ticker.MultipleLocator(100))
            axs[count_ax].yaxis.set_minor_locator(ticker.MultipleLocator(minor_step))
            axs[count_ax].tick_params(axis='x',
                                      which='major',
                                      direction='out',
                                      length=2,
                                      width=1,
                                      color='black',
                                      pad=2,
                                      labelsize=8,
                                      labelcolor='black',
                                      bottom=True,
                                      labelbottom=True,
                                      labelrotation=80)
            axs[count_ax].set_ylim(0, max_ampl // minor_step * minor_step + minor_step)
        plt.show(block=False)

    # def paint_window(self):
    #     import matplotlib.pyplot as plt
    #     import matplotlib.ticker as ticker
    #     x_range, y_range = self.get_plot_pos()
    #     fig, axs = plt.subplots(x_range, y_range, figsize=(16, 9), sharey=True, tight_layout=True)
    #     fig.suptitle("Amplitude distribution")
    #     fig.autofmt_xdate()
    #     for count_ax in range(x_range * y_range):
    #         x = int(count_ax % y_range)
    #         y = int(count_ax / y_range)
    #         # print(x_range, y_range, count_ax, x, y)
    #         if count_ax < self.get_numb_g2():
    #             g2 = list(self.get_g2_list())[count_ax]
    #             freq_list = self.get_g2_freq_list(g2)
    #             ampl_list = self.get_g2_ampl_list(g2)
    #             color_list = self.get_color_bar(self.get_g2_ampl_list(g2))
    #             axs[y][x].bar(freq_list, ampl_list, color=color_list)
    #             axs[y][x].set_title(f"G{g2}")
    #             axs[y][x].set_xlabel("carrier frequency")
    #             axs[y][x].set_ylabel("amplitude")
    #             axs[y][x].autoscale(True)
    #             axs[y][x].grid(which='major', axis='y')
    #             axs[y][x].grid(which='minor', axis='y', linestyle='--')
    #             axs[y][x].yaxis.set_major_locator(ticker.MultipleLocator(500))
    #             axs[y][x].yaxis.set_minor_locator(ticker.MultipleLocator(100))
    #         else:
    #             axs[y][x].remove()
    #     plt.show()
