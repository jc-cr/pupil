'''
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2017  Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
'''

import os
import psutil
import glfw
from pyglui import ui, graph
from plugin import System_Plugin_Base


class System_Graphs(System_Plugin_Base):
    def __init__(self, g_pool, show_cpu=True, show_fps=True, show_conf0=True, show_conf1=True):
        super().__init__(g_pool)
        self.show_cpu = show_cpu
        self.show_fps = show_fps
        self.show_conf0 = show_conf0
        self.show_conf1 = show_conf1
        self.ts = None

    @classmethod
    def icon_info(self):
        return 'pupil_icons', chr(0xe922)

    def init_ui(self):
        self.add_menu()
        self.menu_icon.order = 0.01
        self.menu.label = 'System Graphs'
        self.menu.append(ui.Switch('show_cpu', self, label='Display CPU usage'))
        self.menu.append(ui.Switch('show_fps', self, label='Display frames per second'))
        self.menu.append(ui.Switch('show_conf0', self, label='Display confidence for eye 0'))
        self.menu.append(ui.Switch('show_conf1', self, label='Display confidence for eye 1'))

        # set up performace graphs:
        pid = os.getpid()
        ps = psutil.Process(pid)

        self.cpu_graph = graph.Bar_Graph()
        self.cpu_graph.pos = (20, 130)
        self.cpu_graph.update_fn = ps.cpu_percent
        self.cpu_graph.update_rate = 5
        self.cpu_graph.label = 'CPU %0.1f'

        self.fps_graph = graph.Bar_Graph()
        self.fps_graph.pos = (140, 130)
        self.fps_graph.update_rate = 5
        self.fps_graph.label = "%0.0f FPS"

        self.conf0_graph = graph.Bar_Graph(max_val=1.0)
        self.conf0_graph.pos = (260, 130)
        self.conf0_graph.update_rate = 5
        self.conf0_graph.label = "id0 conf: %0.2f"
        self.conf1_graph = graph.Bar_Graph(max_val=1.0)
        self.conf1_graph.pos = (380, 130)
        self.conf1_graph.update_rate = 5
        self.conf1_graph.label = "id1 conf: %0.2f"

        self.on_window_resize(self.g_pool.main_window)

    def on_window_resize(self, window, *args):
        fb_size = glfw.glfwGetFramebufferSize(window)
        hdpi_factor = float(fb_size[0] / glfw.glfwGetWindowSize(window)[0])

        self.cpu_graph.scale = hdpi_factor
        self.fps_graph.scale = hdpi_factor
        self.conf0_graph.scale = hdpi_factor
        self.conf1_graph.scale = hdpi_factor

        self.cpu_graph.adjust_window_size(*fb_size)
        self.fps_graph.adjust_window_size(*fb_size)
        self.conf0_graph.adjust_window_size(*fb_size)
        self.conf1_graph.adjust_window_size(*fb_size)

    def gl_display(self):
        graphs = (self.cpu_graph, self.fps_graph, self.conf0_graph, self.conf1_graph)
        should_show = (self.show_cpu, self.show_fps, self.show_conf0, self.show_conf1)
        for show, g in zip(should_show, graphs):
            if show:
                g.draw()

    def recent_events(self, events):
        self.cpu_graph.update()
        # update performace graphs
        if 'frame' in events:
            t = events["frame"].timestamp
            if self.ts and t != self.ts:
                dt, self.ts = t-self.ts, t
                try:
                    self.fps_graph.add(1./dt)
                except ZeroDivisionError:
                    pass

                for p in events["pupil_positions"]:
                    (self.conf0_graph if p['id'] == 0 else self.conf1_graph).add(p['confidence'])
            else:
                self.ts = t

    def deinit_ui(self):
        self.remove_menu()
        self.cpu_graph = None
        self.fps_graph = None
        self.conf0_graph = None
        self.conf1_graph = None

    def get_init_dict(self):
        return {'show_cpu': self.show_cpu, 'show_fps': self.show_fps,
                'show_conf0': self.show_conf0, 'show_conf1': self.show_conf1}
