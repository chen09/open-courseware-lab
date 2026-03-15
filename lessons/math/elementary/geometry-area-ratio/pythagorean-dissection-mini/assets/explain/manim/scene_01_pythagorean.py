from manim import *


class Scene01PythagoreanDissection(Scene):
    def construct(self):
        title = Text("Pythagorean Proof by Dissection", font_size=34)
        header = VGroup(title).to_edge(UP, buff=0.16)

        # Move content upward to keep bottom area clear for captions.
        square = Square(side_length=4.0, color=GREY_B, stroke_width=4).shift(LEFT * 2.8 + UP * 0.02)
        P = square.get_corner(UL)
        Q = square.get_corner(UR)
        R = square.get_corner(DR)
        S = square.get_corner(DL)

        # Correct dissection geometry:
        # use the same a split on each side, so corner triangles are right triangles
        # with legs a and b=(L-a), and the center is a true square of side c.
        a_ratio = 0.28

        top_split = P + a_ratio * (Q - P)
        right_split = Q + a_ratio * (R - Q)
        bottom_split = R + a_ratio * (S - R)
        left_split = S + a_ratio * (P - S)

        t1 = Polygon(P, top_split, left_split, color=BLUE_D, fill_color=BLUE_C, fill_opacity=0.45)
        t2 = Polygon(Q, right_split, top_split, color=BLUE_D, fill_color=BLUE_C, fill_opacity=0.45)
        t3 = Polygon(R, bottom_split, right_split, color=BLUE_D, fill_color=BLUE_C, fill_opacity=0.45)
        t4 = Polygon(S, left_split, bottom_split, color=BLUE_D, fill_color=BLUE_C, fill_opacity=0.45)
        center = Polygon(top_split, right_split, bottom_split, left_split, color=GREEN_D, fill_color=GREEN_C, fill_opacity=0.5)

        def tri_area_label(corner, leg1, leg2):
            # Place label near the right-angle corner, away from shared center edges.
            pos = corner + 0.35 * (leg1 - corner) + 0.35 * (leg2 - corner)
            lbl = MathTex(r"\frac{ab}{2}").scale(0.5).move_to(pos)
            lbl.set_stroke(BLACK, width=5, background=True)
            return lbl

        ab2_labels = VGroup(
            tri_area_label(P, top_split, left_split),
            tri_area_label(Q, right_split, top_split),
            tri_area_label(R, bottom_split, right_split),
            tri_area_label(S, left_split, bottom_split),
        )
        c2_label = MathTex("c^2", color=GREEN_D).scale(0.9).move_to(center.get_center())
        # Place (a+b)^2 above the square to avoid overlapping inner geometry.
        outer_label = MathTex("(a+b)^2").scale(0.72).next_to(square, UP, buff=0.14)

        eq1 = MathTex(r"(a+b)^2", r"=", r"4\cdot\frac{ab}{2}", r"+", r"c^2").scale(0.84)
        eq2 = MathTex(r"a^2", r"+", r"2ab", r"+", r"b^2", r"=", r"2ab", r"+", r"c^2").scale(0.84)
        eq3 = MathTex(r"a^2", r"+", r"b^2", r"=", r"c^2", color=GREEN_D).scale(1.02)
        eq_group = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        # Keep formulas above subtitle-safe area in the lower part of the frame.
        eq_group.next_to(square, RIGHT, buff=0.95).shift(UP * 0.42)

        edge_a = MathTex("a", color=BLUE_D).scale(0.62).next_to(Line(P, top_split), UP, buff=0.06)
        edge_b = MathTex("b", color=ORANGE).scale(0.62).next_to(Line(top_split, Q), UP, buff=0.06)
        edge_a_right = MathTex("a", color=BLUE_D).scale(0.62).next_to(Line(Q, right_split), RIGHT, buff=0.06)
        edge_b_right = MathTex("b", color=ORANGE).scale(0.62).next_to(Line(right_split, R), RIGHT, buff=0.06)
        # Mirror labels on the left vertical side as well (top segment is b, bottom segment is a).
        edge_b_left = MathTex("b", color=ORANGE).scale(0.62).next_to(Line(P, left_split), LEFT, buff=0.06)
        edge_a_left = MathTex("a", color=BLUE_D).scale(0.62).next_to(Line(left_split, S), LEFT, buff=0.06)

        c_on_edge_1 = MathTex("c", color=GREEN_D).scale(0.62).move_to((top_split + right_split) / 2 + RIGHT * 0.08 + UP * 0.1)
        c_on_edge_2 = MathTex("c", color=GREEN_D).scale(0.62).move_to((right_split + bottom_split) / 2 + RIGHT * 0.08 + DOWN * 0.02)
        c_on_edge_3 = MathTex("c", color=GREEN_D).scale(0.62).move_to((bottom_split + left_split) / 2 + LEFT * 0.08 + DOWN * 0.08)
        c_on_edge_4 = MathTex("c", color=GREEN_D).scale(0.62).move_to((left_split + top_split) / 2 + LEFT * 0.08 + UP * 0.02)


        self.play(FadeIn(header, shift=DOWN * 0.2))
        self.play(Create(square))
        self.play(
            FadeIn(t1), FadeIn(t2), FadeIn(t3), FadeIn(t4),
            FadeIn(center),
            FadeIn(edge_a), FadeIn(edge_b), FadeIn(edge_a_right), FadeIn(edge_b_right),
            FadeIn(edge_b_left), FadeIn(edge_a_left),
            FadeIn(outer_label),
        )
        self.play(Indicate(outer_label, color=YELLOW_D, scale_factor=1.15), Indicate(square, color=YELLOW_D), run_time=1.2)
        # Use ghost-motion mapping instead of arrows for (a+b)^2 -> equation.
        outer_ghost = outer_label.copy().set_color(YELLOW_D).set_opacity(0.92)
        outer_ghost.set_z_index(10)
        self.play(FadeIn(outer_ghost), run_time=0.18)
        self.play(outer_ghost.animate.scale(0.9).move_to(eq1[0].get_center()), Write(eq1[1]), run_time=0.8)
        self.play(ReplacementTransform(outer_ghost, eq1[0]), run_time=0.35)
        self.play(FadeOut(outer_label), run_time=0.25)

        self.play(Write(c2_label), run_time=0.6)
        self.play(LaggedStart(*[Write(lbl) for lbl in ab2_labels], lag_ratio=0.16), run_time=1.25)
        self.play(FadeIn(c_on_edge_1), FadeIn(c_on_edge_2), FadeIn(c_on_edge_3), FadeIn(c_on_edge_4))
        self.wait(0.15)

        # Replace arrows with a cleaner "ghost triangle gather" motion to explain 4*(ab/2).
        tri_ghosts = VGroup(
            *[
                tri.copy()
                .set_fill(color=YELLOW_D, opacity=0.14)
                .set_stroke(color=YELLOW_D, width=3, opacity=0.75)
                for tri in (t1, t2, t3, t4)
            ]
        )
        gather_offsets = [UP * 0.35 + LEFT * 0.35, UP * 0.35 + RIGHT * 0.35, DOWN * 0.35 + LEFT * 0.35, DOWN * 0.35 + RIGHT * 0.35]
        for g in tri_ghosts:
            g.set_z_index(8)
        # Story order: flash triangles first, gather them, then flash/move c^2.
        self.play(
            Indicate(t1, color=YELLOW_D),
            Indicate(t2, color=YELLOW_D),
            Indicate(t3, color=YELLOW_D),
            Indicate(t4, color=YELLOW_D),
            run_time=0.7,
        )
        self.play(FadeIn(tri_ghosts), run_time=0.25)
        self.play(
            *[
                tri_ghosts[i].animate.rotate((i - 1.5) * 0.45).scale(0.33).move_to(eq1[2].get_center() + gather_offsets[i])
                for i in range(4)
            ],
            run_time=1.2,
        )
        mid_ab2 = MathTex(r"\frac{ab}{2}", color=YELLOW_D).scale(0.78).move_to(eq1[2].get_center())
        self.play(Write(mid_ab2), run_time=0.45)
        self.play(Write(eq1[2]), FadeOut(mid_ab2), FadeOut(tri_ghosts), run_time=0.75)

        # Then flash c^2 and move the center square itself (not text) as a ghost.
        self.play(Indicate(c2_label, color=GREEN_D, scale_factor=1.12), Indicate(center, color=GREEN_D), run_time=0.7)
        self.play(Write(eq1[3]), run_time=0.25)
        center_ghost = center.copy().set_fill(GREEN_C, opacity=0.2).set_stroke(GREEN_E, width=4, opacity=0.95)
        center_ghost.set_z_index(10)
        self.play(FadeIn(center_ghost), run_time=0.15)
        self.play(center_ghost.animate.scale(0.24).move_to(eq1[4].get_center()), run_time=0.62)
        self.play(FadeOut(center_ghost), FadeIn(eq1[4]), run_time=0.32)

        # (a+b)(a+b) expansion cue: first formula -> second formula LHS.
        expand_arrow = CurvedArrow(
            eq1[0].get_bottom() + DOWN * 0.03,
            VGroup(eq2[0], eq2[1], eq2[2], eq2[3], eq2[4]).get_top() + UP * 0.05,
            angle=-0.35,
            color=YELLOW_D,
            stroke_width=4,
        )
        self.play(Create(expand_arrow), run_time=0.55)
        self.play(
            TransformFromCopy(eq1[0], eq2[0]),
            Write(eq2[1]),
            Write(eq2[2]),
            Write(eq2[3]),
            Write(eq2[4]),
            run_time=1.0,
        )
        self.play(FadeOut(expand_arrow), Write(eq2[5]), run_time=0.25)

        # 4*ab/2 -> 2ab and c^2 carry-over cue on RHS.
        rhs_arrow = CurvedArrow(
            eq1[2].get_bottom() + DOWN * 0.02,
            eq2[6].get_top() + UP * 0.06,
            angle=-0.32,
            color=YELLOW_D,
            stroke_width=4,
        )
        self.play(Create(rhs_arrow), run_time=0.5)
        self.play(
            TransformFromCopy(eq1[2], eq2[6]),
            Write(eq2[7]),
            TransformFromCopy(eq1[4], eq2[8]),
            run_time=0.9,
        )
        self.play(FadeOut(rhs_arrow), run_time=0.2)

        # Cancel 2ab on both sides with strike animation.
        self.play(Indicate(eq2[2], color=RED_D), Indicate(eq2[6], color=RED_D), run_time=0.6)
        cancel_left = Line(eq2[2].get_corner(UL), eq2[2].get_corner(DR), color=RED_D, stroke_width=6)
        cancel_right = Line(eq2[6].get_corner(UL), eq2[6].get_corner(DR), color=RED_D, stroke_width=6)
        self.play(Create(cancel_left), Create(cancel_right), run_time=0.45)
        self.play(FadeOut(eq2[2]), FadeOut(eq2[6]), FadeOut(eq2[7]), FadeOut(cancel_left), FadeOut(cancel_right), run_time=0.65)

        # Build final formula from remaining terms.
        self.play(
            TransformFromCopy(eq2[0], eq3[0]),
            TransformFromCopy(eq2[1], eq3[1]),
            TransformFromCopy(eq2[4], eq3[2]),
            TransformFromCopy(eq2[5], eq3[3]),
            TransformFromCopy(eq2[8], eq3[4]),
            run_time=1.0,
        )
        self.play(Indicate(eq3, color=GREEN_D), run_time=0.8)
        self.wait(1.2)
