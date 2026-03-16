from manim import *


class Scene01MirrorClassroom(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        title = Text("Mirror Classroom: X fixed, Y changes", font_size=42, color=WHITE)
        title.to_edge(UP).shift(DOWN * 0.2)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        frame = Rectangle(width=11.5, height=4.6, color="#94a3b8", stroke_width=2)
        frame.shift(DOWN * 0.3)
        rear_wall = Line(frame.get_corner(UL) + RIGHT * 0.8, frame.get_corner(DL) + RIGHT * 0.8, color="#64748b", stroke_width=8)
        mirror = Line(frame.get_corner(UR) + LEFT * 0.8, frame.get_corner(DR) + LEFT * 0.8, color=WHITE, stroke_width=6)

        rear_label = Text("rear wall (3m)", font_size=24, color="#cbd5e1").next_to(rear_wall, UP + LEFT, buff=0.2)
        mirror_label = Text("mirror", font_size=24, color="#cbd5e1").next_to(mirror, UP + RIGHT, buff=0.2)

        self.play(Create(frame), run_time=0.6)
        self.play(Create(rear_wall), Create(mirror), FadeIn(rear_label), FadeIn(mirror_label), run_time=0.8)

        d_tracker = ValueTracker(2.0)
        eye_y = frame.get_center()[1] + 0.35
        mirror_x = mirror.get_center()[0]
        room_depth = 8.0
        px_per_m = 0.86

        def eye_x():
            return mirror_x - d_tracker.get_value() * px_per_m

        eye_dot = always_redraw(lambda: Dot(point=[eye_x(), eye_y, 0], radius=0.08, color="#ef4444"))
        eye_label = always_redraw(
            lambda: Text("eye", font_size=20, color="#fecaca").next_to(eye_dot, UP + RIGHT, buff=0.08)
        )

        x_len = 0.75 * px_per_m
        x_segment = always_redraw(
            lambda: Line(
                [mirror_x, eye_y - x_len / 2, 0],
                [mirror_x, eye_y + x_len / 2, 0],
                color="#22c55e",
                stroke_width=11,
            )
        )
        x_text = always_redraw(
            lambda: Text("X = 75 cm", font_size=24, color="#22c55e").next_to(x_segment, RIGHT, buff=0.2)
        )

        def y_len():
            y_m = 3.0 * d_tracker.get_value() / (d_tracker.get_value() + room_depth)
            return y_m * px_per_m

        y_offset = 0.08
        y_segment = always_redraw(
            lambda: Line(
                [mirror_x, eye_y - y_offset, 0],
                [mirror_x, eye_y - y_offset - y_len(), 0],
                color="#60a5fa",
                stroke_width=11,
            )
        )

        y_value = DecimalNumber(60.0, num_decimal_places=1, font_size=26, color="#60a5fa")
        y_suffix = Text("cm", font_size=24, color="#93c5fd")
        y_group = VGroup(Text("Y =", font_size=24, color="#60a5fa"), y_value, y_suffix).arrange(RIGHT, buff=0.08)
        y_group.add_updater(lambda mob: mob.next_to(y_segment, RIGHT, buff=0.2))
        y_value.add_updater(lambda n: n.set_value(100 * 3.0 * d_tracker.get_value() / (d_tracker.get_value() + room_depth)))

        ray_x_top = always_redraw(
            lambda: DashedLine(
                [eye_x(), eye_y, 0],
                [mirror_x, eye_y + x_len / 2, 0],
                color="#22c55e",
                dash_length=0.15,
            )
        )
        ray_x_bottom = always_redraw(
            lambda: DashedLine(
                [eye_x(), eye_y, 0],
                [mirror_x, eye_y - x_len / 2, 0],
                color="#22c55e",
                dash_length=0.15,
            )
        )
        ray_y_top = always_redraw(
            lambda: DashedLine(
                [eye_x(), eye_y, 0],
                [mirror_x, eye_y - y_offset, 0],
                color="#60a5fa",
                dash_length=0.12,
            )
        )
        ray_y_bottom = always_redraw(
            lambda: DashedLine(
                [eye_x(), eye_y, 0],
                [mirror_x, eye_y - y_offset - y_len(), 0],
                color="#60a5fa",
                dash_length=0.12,
            )
        )

        formula_box = RoundedRectangle(width=5.9, height=1.8, corner_radius=0.18, color="#334155")
        formula_box.set_fill("#0b1220", opacity=0.95)
        formula_box.to_corner(DR).shift(LEFT * 0.25 + UP * 0.25)
        f1 = MathTex(r"X=\frac{150}{2}=75\mathrm{cm}", color="#22c55e").scale(0.7).move_to(formula_box.get_center() + UP * 0.35)
        f2 = MathTex(r"Y(d)=\frac{3d}{d+8}\,\mathrm{m}", color="#60a5fa").scale(0.7).move_to(formula_box.get_center() + DOWN * 0.35)

        d_line = always_redraw(
            lambda: DoubleArrow(
                start=[eye_x(), frame.get_bottom()[1] - 0.25, 0],
                end=[mirror_x, frame.get_bottom()[1] - 0.25, 0],
                buff=0.0,
                color="#e2e8f0",
                stroke_width=3,
            )
        )
        d_num = DecimalNumber(2.0, num_decimal_places=1, font_size=28, color="#e2e8f0")
        d_num.add_updater(lambda n: n.set_value(d_tracker.get_value()))
        d_label = VGroup(Text("d =", font_size=26, color="#e2e8f0"), d_num, Text("m", font_size=24, color="#e2e8f0")).arrange(
            RIGHT, buff=0.08
        )
        d_label.add_updater(lambda m: m.next_to(d_line, DOWN, buff=0.12))

        self.play(FadeIn(eye_dot), FadeIn(eye_label), run_time=0.4)
        self.play(Create(x_segment), Create(y_segment), run_time=0.6)
        self.play(Create(ray_x_top), Create(ray_x_bottom), Create(ray_y_top), Create(ray_y_bottom), run_time=0.7)
        self.play(FadeIn(x_text), FadeIn(y_group), run_time=0.4)
        self.play(Create(d_line), FadeIn(d_label), run_time=0.6)
        self.play(FadeIn(formula_box), Write(f1), Write(f2), run_time=1.0)
        self.wait(0.4)

        self.play(d_tracker.animate.set_value(7.8), run_time=5.2, rate_func=linear)
        self.wait(0.6)
        self.play(d_tracker.animate.set_value(2.0), run_time=2.8, rate_func=smooth)
        self.wait(0.6)
