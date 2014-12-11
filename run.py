"""The cs143sim run script, with -c/--case and -d/--duration options

.. moduleauthor: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""
import matplotlib.pyplot as plt

from cs143sim.simulation import Controller


NUMBER_X_STEPS = 100


def graph_flow_rate_or_packet_loss(case, category, controller, duration, x_step):
    title = 'Case ' + str(case) + ' ' + category
    figure, axes = plt.subplots()
    figure.canvas.set_window_title(title)
    axes.set_title(title)
    axes.set_xlabel('Time (s)')
    units = 'Mbps' if category == 'Flow Rate' else 'packets / second'
    axes.set_ylabel(category + ' (' + units + ')')
    record_name = '_'.join(category.lower().split(' '))
    record = controller.__dict__[record_name]
    for actor in sorted(record.keys()):
        x = [0]
        y = [0]
        for time, value in record[actor]:
            while time > x[-1]:
                x.append(x[-1] + x_step)
                y.append(0)
            y[-1] += value if value else 1
        while duration > x[-1]:
            x.append(x[-1] + x_step)
            y.append(0)
        x = [time / 1000.0 for time in x]
        y = [value * 1.0 / x_step for value in y]
        axes.plot(x, y, label=actor.name)
    axes.legend()


def graph_packet_delay_or_window_size(case, category, controller, x_step):
    title = 'Case ' + str(case) + ' ' + category
    figure, axes = plt.subplots()
    figure.canvas.set_window_title(title)
    axes.set_title(title)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel(category + ' (ms)')
    record_name = '_'.join(category.lower().split(' '))
    record = controller.__dict__[record_name]
    for actor in sorted(record.keys()):
        x = [0]
        y = [0]
        for time, value in record[actor]:
            x.append(time)
            y.append(value)
        length = len(x)
        smooth_x = []
        smooth_y = []
        init_time = 0
        sum_y = 0
        for i in range(length):
            if x[i] > (init_time + x_step):
                exceed = (int(x[i]) - (init_time + x_step)) / x_step
                sum_y += y[i - 1] * (init_time + x_step - x[i - 1])
                smooth_x.append(float(init_time) / float(1000))
                smooth_y.append(sum_y / x_step)
                for j in range(exceed - 1):
                    smooth_x.append(float(init_time + (j + 1) * x_step) / float(1000))
                    smooth_y.append(y[i - 1])
                init_time += x_step * (exceed + 1)
                sum_y = y[i - 1] * (x[i] - init_time)
            elif i > 0:
                sum_y += y[i - 1] * (x[i] - max(init_time, x[i - 1]))
        axes.plot(smooth_x, smooth_y, label=actor.name)
    axes.legend()


def graph_buffer_occupancy(case, category, controller, x_step):
    title = 'Case ' + str(case) + ' ' + category
    figure, axes = plt.subplots()
    figure.canvas.set_window_title(title)
    axes.set_title(title)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel(category + ' (packets)')
    line_color = 'k'
    line_colors = axes._get_lines.color_cycle
    record_name = '_'.join(category.lower().split(' '))
    record = controller.__dict__[record_name]
    for actor in sorted(record.keys()):
        x = [0]
        y = [0]
        for time, value in record[actor]:
            x.append(time)
            y.append(value)
        length = len(x)
        smooth_x = []
        smooth_y = []
        init_time = 0
        sum_y = 0
        for i in range(length):
            if x[i] > (init_time + x_step):
                exceed = (int(x[i]) - (init_time + x_step)) / x_step
                sum_y += y[i - 1] * (init_time + x_step - x[i - 1])
                smooth_x.append(float(init_time) / float(1000))
                smooth_y.append(sum_y / x_step)
                for j in range(exceed - 1):
                    smooth_x.append(float(init_time + (j + 1) * x_step) / float(1000))
                    smooth_y.append(y[i - 1])
                init_time += x_step * (exceed + 1)
                sum_y = y[i - 1] * (x[i] - init_time)
            elif i > 0:
                sum_y += y[i - 1] * (x[i] - max(init_time, x[i - 1]))
        if 'a' in actor.name:
            line_color = next(line_colors)
        line_style = '-' if 'a' in actor.name else ':'
        axes.plot(smooth_x, smooth_y, line_color + line_style, label=actor.name)
    axes.legend()


def graph_link_rate(case, category, controller, x_step):
    title = 'Case ' + str(case) + ' ' + category
    figure, axes = plt.subplots()
    figure.canvas.set_window_title(title)
    axes.set_title(title)
    axes.set_xlabel('Time (s)')
    axes.set_ylabel(category + ' (Mbps)')
    line_color = 'k'
    line_colors = axes._get_lines.color_cycle
    record_name = '_'.join(category.lower().split(' '))
    record = controller.__dict__[record_name]
    for actor in sorted(record.keys()):
        x = [0]
        y = [0]
        for time, value in record[actor]:
            while time > x[-1]:
                x.append(x[-1] + x_step)
                y.append(0)
            y[-1] += value if value else 1
        x = [time / 1000.0 for time in x]
        y = [value * 1.0 * controller.links[actor.name].rate / x_step for value in y]
        if 'a' in actor.name:
            line_color = next(line_colors)
        line_style = '-' if 'a' in actor.name else ':'
        axes.plot(x, y, line_color + line_style, label=actor.name)
    axes.legend()


def run():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-c', '--case', dest='case', help='simulation case number')
    parser.add_argument('-d', '--duration', dest='duration', help='simulation duration in seconds')
    arguments = parser.parse_args()
    case = arguments.case if arguments.case else 0
    duration = arguments.duration if arguments.duration else 10
    controller = Controller(case='cs143sim/cases/case' + str(case) + '.txt')
    controller.run(until=duration)
    x_step = duration / NUMBER_X_STEPS
    graph_buffer_occupancy(case, 'Buffer Occupancy', controller, x_step)
    graph_flow_rate_or_packet_loss(case, 'Flow Rate', controller, duration, x_step)
    graph_link_rate(case, 'Link Rate', controller, x_step)
    graph_packet_delay_or_window_size(case, 'Packet Delay', controller, x_step)
    graph_flow_rate_or_packet_loss(case, 'Packet Loss', controller, duration, x_step)
    graph_packet_delay_or_window_size(case, 'Window Size', controller, x_step)
    plt.show()


if __name__ == '__main__':
    run()
