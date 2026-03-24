from pathlib import Path

from manim import *
from pydub import AudioSegment

SCRIPT_DIR = Path(__file__).resolve().parent

config.background_color = "#0B1020"
config.video_dir = str(SCRIPT_DIR)
config.partial_movie_dir = str(SCRIPT_DIR / "partial_movie_files" / "{quality}" / "{scene_name}")

ZH_FONT = "Noto Sans HK"
EN_FONT = "Tahoma"
CODE_FONT = "Consolas"
AUDIO_DIR = SCRIPT_DIR / "audio"
COVER_PATH = SCRIPT_DIR / "bookcover.png"


def zh_text(content: str, font_size: int, color=WHITE) -> Text:
    return Text(content, font=ZH_FONT, font_size=font_size, color=color, disable_ligatures=True)


def en_text(content: str, font_size: int, color=WHITE) -> Text:
    return Text(content, font=EN_FONT, font_size=font_size, color=color, disable_ligatures=True)


def code_text(content: str, font_size: int, color=WHITE) -> Text:
    return Text(content, font=CODE_FONT, font_size=font_size, color=color, disable_ligatures=True)


def mixed_text(content: str, font_size: int, color=WHITE, english_terms: list[str] | None = None) -> Text:
    t2f = {term: EN_FONT for term in (english_terms or [])}
    return Text(
        content,
        font=ZH_FONT,
        font_size=font_size,
        color=color,
        t2f=t2f,
        disable_ligatures=True,
    )


def make_code_row(input_part: str, output_part: str, color=WHITE) -> VGroup:
    left = code_text(input_part, font_size=24, color=color)
    arrow = code_text("->", font_size=22, color=GREY_A)
    right = code_text(output_part, font_size=24, color=color)
    return VGroup(left, arrow, right).arrange(RIGHT, buff=0.22)


def make_panel(title: str, color: str, width: float, height: float, terms: list[str]) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=0.12,
    )
    label = mixed_text(title, font_size=22, color=color, english_terms=terms)
    label.next_to(box, UP, buff=0.18)
    return VGroup(box, label)


def make_boolean_cube() -> tuple[VGroup, dict[str, VGroup], Polygon]:
    points = {
        "000": np.array([-4.8, -1.1, 0.0]),
        "001": np.array([-3.4, -1.1, 0.0]),
        "010": np.array([-4.8, 0.3, 0.0]),
        "011": np.array([-3.4, 0.3, 0.0]),
        "100": np.array([-3.9, -0.4, 0.0]),
        "101": np.array([-2.5, -0.4, 0.0]),
        "110": np.array([-3.9, 1.0, 0.0]),
        "111": np.array([-2.5, 1.0, 0.0]),
    }

    edge_pairs = [
        ("000", "001"),
        ("001", "011"),
        ("011", "010"),
        ("010", "000"),
        ("100", "101"),
        ("101", "111"),
        ("111", "110"),
        ("110", "100"),
        ("000", "100"),
        ("001", "101"),
        ("010", "110"),
        ("011", "111"),
    ]
    edges = VGroup(
        *[
            Line(points[start], points[end], color=BLUE_D, stroke_width=4)
            for start, end in edge_pairs
        ]
    )

    nodes: dict[str, VGroup] = {}
    for name, position in points.items():
        dot = Dot(point=position, radius=0.08, color=WHITE)
        label = code_text(name, font_size=20, color=GREY_A)
        label.next_to(dot, DOWN if name.endswith("0") else UP, buff=0.12)
        nodes[name] = VGroup(dot, label)

    face = Polygon(
        points["100"],
        points["101"],
        points["111"],
        points["110"],
        stroke_color=GOLD_B,
        stroke_width=4,
        fill_color=GOLD_D,
        fill_opacity=0.0,
    )
    cube = VGroup(edges, face, *nodes.values())
    return cube, nodes, face


def make_truth_table_content() -> VGroup:
    header = VGroup(
        code_text("abc", font_size=18, color=GREY_A),
        code_text("y", font_size=18, color=GREY_A),
    ).arrange(RIGHT, buff=0.5)

    rows = VGroup(
        *[
            VGroup(code_text(bits, 20), code_text(value, 20, color=YELLOW_B)).arrange(RIGHT, buff=0.55)
            for bits, value in [
                ("000", "0"),
                ("001", "1"),
                ("010", "0"),
                ("011", "1"),
                ("100", "1"),
                ("101", "1"),
            ]
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return VGroup(header, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)


def make_kmap_content() -> tuple[VGroup, VGroup]:
    cols = VGroup(*[code_text(label, 16, color=GREY_A) for label in ["00", "01", "11", "10"]]).arrange(RIGHT, buff=0.14)
    rows = VGroup(*[code_text(label, 16, color=GREY_A) for label in ["0", "1"]]).arrange(DOWN, buff=0.4)

    cells = VGroup()
    values = [1, 1, 1, 1, 0, 1, 0, 0]
    for value in values:
        square = Square(side_length=0.52, stroke_color=BLUE_D, stroke_width=2, fill_opacity=0.0)
        label = code_text(str(value), 18, color=WHITE if value else GREY_B)
        cells.add(VGroup(square, label.move_to(square)))

    cells.arrange_in_grid(rows=2, cols=4, buff=0.08)
    cells[0:4].set_fill(GOLD_D, opacity=0.28)
    highlight = SurroundingRectangle(cells[0:4], color=YELLOW_B, buff=0.06, corner_radius=0.1)

    cols.next_to(cells, UP, buff=0.12)
    rows.next_to(cells, LEFT, buff=0.16)
    content = VGroup(cols, rows, cells, highlight)
    return content, highlight


def make_tree_content() -> tuple[VGroup, VGroup]:
    root = Circle(radius=0.22, color=PURPLE_B, fill_color=PURPLE_D, fill_opacity=0.22)
    root_label = code_text("a", 20).move_to(root)
    root_group = VGroup(root, root_label).move_to(UP * 1.15)

    left = Circle(radius=0.2, color=BLUE_B, fill_color=BLUE_D, fill_opacity=0.18)
    left_label = code_text("b", 18).move_to(left)
    left_group = VGroup(left, left_label).move_to(LEFT * 0.9 + UP * 0.25)

    right = Circle(radius=0.2, color=BLUE_B, fill_color=BLUE_D, fill_opacity=0.18)
    right_label = code_text("b", 18).move_to(right)
    right_group = VGroup(right, right_label).move_to(RIGHT * 0.9 + UP * 0.25)

    leaves = VGroup()
    leaf_specs = [
        (LEFT * 1.4 + DOWN * 0.8, "0"),
        (LEFT * 0.4 + DOWN * 0.8, "1"),
        (RIGHT * 0.4 + DOWN * 0.8, "1"),
        (RIGHT * 1.4 + DOWN * 0.8, "1"),
    ]
    for position, value in leaf_specs:
        circle = Circle(radius=0.16, color=TEAL_B, fill_color=TEAL_D, fill_opacity=0.16)
        label = code_text(value, 16).move_to(circle)
        leaves.add(VGroup(circle, label).move_to(position))

    lines = VGroup(
        Line(root_group.get_bottom(), left_group.get_top(), color=GREY_B, stroke_width=3),
        Line(root_group.get_bottom(), right_group.get_top(), color=GREY_B, stroke_width=3),
        Line(left_group.get_bottom(), leaves[0].get_top(), color=GREY_B, stroke_width=3),
        Line(left_group.get_bottom(), leaves[1].get_top(), color=GREY_B, stroke_width=3),
        Line(right_group.get_bottom(), leaves[2].get_top(), color=GREY_B, stroke_width=3),
        Line(right_group.get_bottom(), leaves[3].get_top(), color=GREY_B, stroke_width=3),
    )
    tree = VGroup(lines, root_group, left_group, right_group, leaves)
    return tree, root_group


class Video02BooleanFunctionBasics(Scene):
    def construct(self):
        self.show_book_intro()
        self.create_header()
        self.show_title()
        self.show_hypercube_basics()
        self.show_two_level_description()
        self.show_representation_forms()
        self.show_takeaway()

    def start_voiceover(self, filename: str) -> float:
        audio_path = AUDIO_DIR / filename
        self.add_sound(str(audio_path))
        return AudioSegment.from_file(audio_path).duration_seconds

    def finish_voiceover(self, duration: float, elapsed: float, padding: float = 0.2):
        remaining = duration - elapsed
        if remaining > 0:
            self.wait(remaining + padding)

    def show_book_intro(self):
        voice_duration = self.start_voiceover("00_book_intro.mp3")
        elapsed = 0.0

        intro_brand = zh_text("香港編程學會", font_size=20, color=WHITE)
        intro_brand.to_corner(UL, buff=0.22)

        intro_producer = VGroup(
            zh_text("制片人", font_size=16, color=GREY_A),
            en_text("Peter", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        intro_producer.to_edge(LEFT, buff=0.16)
        intro_producer.shift(DOWN * 0.9)

        cover = ImageMobject(str(COVER_PATH)).set_height(5.35)
        cover.move_to(UP * 0.2)

        summary_title = zh_text("本集重點", font_size=28, color=GOLD_B)
        summary_line = mixed_text(
            "Hypercube  |  Implicant  |  Truth Table  |  Karnaugh Map",
            font_size=18,
            color=GREY_A,
            english_terms=["Hypercube", "Implicant", "Truth Table", "Karnaugh Map"],
        )
        summary = VGroup(summary_title, summary_line).arrange(DOWN, buff=0.14)
        summary.to_edge(DOWN, buff=0.42)

        self.play(
            FadeIn(cover, shift=UP * 0.15),
            FadeIn(intro_brand, shift=UP * 0.1),
            FadeIn(intro_producer, shift=RIGHT * 0.1),
            run_time=1.5,
        )
        elapsed += 1.5
        self.play(FadeIn(summary, shift=UP * 0.15), run_time=1.0)
        elapsed += 1.0
        self.wait(0.8)
        elapsed += 0.8
        self.finish_voiceover(voice_duration, elapsed, padding=0.3)
        self.play(FadeOut(cover), FadeOut(summary), FadeOut(intro_brand), FadeOut(intro_producer), run_time=0.8)

    def create_header(self):
        cover = ImageMobject(str(COVER_PATH)).set_height(0.92)
        book_title = VGroup(
            en_text("Technology Mapping", font_size=16, color=WHITE),
            en_text("for LUT-Based FPGA", font_size=16, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)

        self.header_left = Group(cover, book_title).arrange(RIGHT, buff=0.16, aligned_edge=UP)
        self.header_left.to_corner(UL, buff=0.22)

        brand = zh_text("香港編程學會", font_size=22, color=WHITE)
        self.header_right = brand.to_corner(UR, buff=0.28)

        self.add(self.header_left, self.header_right)
        self.add_foreground_mobjects(self.header_left, self.header_right)

    def show_title(self):
        voice_duration = self.start_voiceover("01_title.mp3")
        elapsed = 0.0

        title = zh_text("第 2 集", font_size=42, color=BLUE_B)
        subtitle = mixed_text("Boolean Function 表示法入門", font_size=54, english_terms=["Boolean Function"])
        tagline = mixed_text(
            "由 hypercube 到 binary decision tree",
            font_size=27,
            color=GREY_B,
            english_terms=["hypercube", "binary decision tree"],
        )
        group = VGroup(title, subtitle, tagline).arrange(DOWN, buff=0.22)

        self.play(FadeIn(group, shift=UP), run_time=1.4)
        elapsed += 1.4
        self.wait(0.8)
        elapsed += 0.8
        self.play(group.animate.scale(0.7).to_edge(UP, buff=1.03), run_time=0.9)
        elapsed += 0.9
        self.finish_voiceover(voice_duration, elapsed)
        self.title_group = group

    def show_hypercube_basics(self):
        voice_duration = self.start_voiceover("02_hypercube.mp3")
        elapsed = 0.0

        section_title = mixed_text(
            "Hypercube、Cube、Implicant 同 Minterm",
            font_size=31,
            color=BLUE_B,
            english_terms=["Hypercube", "Cube", "Implicant", "Minterm"],
        )
        section_title.next_to(self.title_group, DOWN, buff=0.36)

        cube, nodes, face = make_boolean_cube()
        point_ring = Circle(radius=0.23, color=YELLOW_B, stroke_width=4).move_to(nodes["101"][0].get_center())

        note_1 = VGroup(
            mixed_text("每個點都係 1 個 minterm", font_size=24, color=GREY_A, english_terms=["minterm"]),
            code_text("101", font_size=28, color=YELLOW_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        note_2 = VGroup(
            mixed_text("一個面可以表示 1 個 cube", font_size=24, color=GREY_A, english_terms=["cube"]),
            code_text("1--", font_size=28, color=GOLD_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        note_3 = mixed_text(
            "如果覆蓋到嘅點全部屬於 ON 或 DC，呢個 cube 就係 implicant。",
            font_size=22,
            color=GREY_A,
            english_terms=["ON", "DC", "cube", "implicant"],
        )

        notes = VGroup(note_1, note_2, note_3).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        notes.move_to(RIGHT * 3.25 + DOWN * 0.25)

        self.play(FadeIn(section_title, shift=UP * 0.15), FadeIn(cube, shift=LEFT * 0.2), run_time=1.3)
        elapsed += 1.3
        self.play(Create(point_ring), Indicate(nodes["101"][0], color=YELLOW), FadeIn(note_1, shift=RIGHT * 0.15), run_time=1.0)
        elapsed += 1.0
        self.play(
            face.animate.set_fill(GOLD_D, opacity=0.28),
            *[nodes[name][0].animate.set_color(GOLD_B) for name in ["100", "101", "110", "111"]],
            FadeIn(note_2, shift=RIGHT * 0.15),
            run_time=1.1,
        )
        elapsed += 1.1
        self.play(FadeIn(note_3, shift=UP * 0.12), run_time=0.9)
        elapsed += 0.9
        self.wait(0.8)
        elapsed += 0.8
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(section_title), FadeOut(cube), FadeOut(point_ring), FadeOut(notes), run_time=0.8)

    def show_two_level_description(self):
        voice_duration = self.start_voiceover("03_two_level.mp3")
        elapsed = 0.0

        left_panel = make_panel("Minterm 列表", TEAL_B, width=4.2, height=4.6, terms=["Minterm"])
        right_panel = make_panel("Two-Level 壓縮", GOLD_B, width=4.2, height=4.6, terms=["Two-Level"])
        panels = VGroup(left_panel, right_panel).arrange(RIGHT, buff=1.1)
        panels.move_to(DOWN * 0.1)

        left_rows = VGroup(
            *[
                make_code_row(bits, "1")
                for bits in ["0001", "0101", "1001", "1011", "1101", "1111"]
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left_rows.move_to(left_panel[0])

        right_rows = VGroup(
            make_code_row("0-01", "1", color=YELLOW_B),
            make_code_row("1--1", "1", color=YELLOW_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        right_rows.move_to(right_panel[0])

        arrow = Arrow(left_panel[0].get_right(), right_panel[0].get_left(), buff=0.22, stroke_width=4, color=GREY_B)
        dash_note = mixed_text("dash 代表嗰個變數唔重要。", font_size=22, color=GREY_B, english_terms=["dash"])
        dash_note.next_to(right_panel[0], DOWN, buff=0.34)

        compression_note = mixed_text(
            "多個 minterm 可以壓縮成少量 implicant。",
            font_size=23,
            color=GREY_A,
            english_terms=["minterm", "implicant"],
        )
        compression_note.next_to(panels, UP, buff=0.38)

        self.play(FadeIn(compression_note, shift=UP * 0.15), FadeIn(left_panel, shift=UP * 0.15), run_time=1.0)
        elapsed += 1.0
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in left_rows], lag_ratio=0.1), run_time=1.3)
        elapsed += 1.3
        self.play(GrowArrow(arrow), FadeIn(right_panel, shift=UP * 0.15), run_time=0.9)
        elapsed += 0.9
        self.play(FadeIn(right_rows, shift=LEFT * 0.1), FadeIn(dash_note, shift=UP * 0.12), run_time=1.0)
        elapsed += 1.0
        self.wait(0.8)
        elapsed += 0.8
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(compression_note), FadeOut(left_panel), FadeOut(left_rows), FadeOut(arrow), FadeOut(right_panel), FadeOut(right_rows), FadeOut(dash_note), run_time=0.8)

    def show_representation_forms(self):
        voice_duration = self.start_voiceover("04_representations.mp3")
        elapsed = 0.0

        headline = mixed_text(
            "同一個 Boolean function，可以有唔同表示法",
            font_size=30,
            color=BLUE_B,
            english_terms=["Boolean function"],
        )
        headline.next_to(self.title_group, DOWN, buff=0.34)

        truth_panel = make_panel("Truth Table", TEAL_B, width=3.35, height=4.55, terms=["Truth Table"])
        kmap_panel = make_panel("Karnaugh Map", GOLD_B, width=3.35, height=4.55, terms=["Karnaugh Map"])
        tree_panel = make_panel("Binary Decision Tree", PURPLE_B, width=3.35, height=4.55, terms=["Binary Decision Tree"])
        panels = VGroup(truth_panel, kmap_panel, tree_panel).arrange(RIGHT, buff=0.55)
        panels.move_to(DOWN * 0.35)

        truth_content = make_truth_table_content().move_to(truth_panel[0])
        kmap_content, kmap_highlight = make_kmap_content()
        kmap_content.move_to(kmap_panel[0])
        tree_content, tree_root = make_tree_content()
        tree_content.move_to(tree_panel[0].get_center() + DOWN * 0.05)

        bottom_note = mixed_text(
            "truth table 最直觀，K-map 方便 grouping，decision tree 方便結構化表示。",
            font_size=21,
            color=GREY_A,
            english_terms=["truth table", "K-map", "grouping", "decision tree"],
        )
        bottom_note.to_edge(DOWN, buff=0.36)

        self.play(FadeIn(headline, shift=UP * 0.15), run_time=0.8)
        elapsed += 0.8
        self.play(FadeIn(truth_panel, shift=UP * 0.15), FadeIn(truth_content, shift=UP * 0.1), run_time=1.0)
        elapsed += 1.0
        self.play(FadeIn(kmap_panel, shift=UP * 0.15), FadeIn(kmap_content, shift=UP * 0.1), run_time=1.0)
        elapsed += 1.0
        self.play(FadeIn(tree_panel, shift=UP * 0.15), FadeIn(tree_content, shift=UP * 0.1), run_time=1.0)
        elapsed += 1.0
        self.play(Indicate(kmap_highlight, color=YELLOW), Indicate(tree_root[0], color=PURPLE_B), run_time=1.0)
        elapsed += 1.0
        self.play(FadeIn(bottom_note, shift=UP * 0.12), run_time=0.8)
        elapsed += 0.8
        self.wait(0.8)
        elapsed += 0.8
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(headline), FadeOut(panels), FadeOut(truth_content), FadeOut(kmap_content), FadeOut(tree_content), FadeOut(bottom_note), run_time=0.8)

    def show_takeaway(self):
        voice_duration = self.start_voiceover("05_takeaway.mp3")
        elapsed = 0.0

        takeaway = mixed_text(
            "表示法唔只係記錄方式\n而係影響之後點樣優化",
            font_size=30,
            color=GOLD_B,
            english_terms=["optimize"],
        )
        takeaway.move_to(UP * 0.75)

        points = VGroup(
            mixed_text("點對應 minterm", font_size=26, color=GREY_A, english_terms=["minterm"]),
            mixed_text("多個相鄰點形成 cube", font_size=26, color=GREY_A, english_terms=["cube"]),
            mixed_text("唔同表示法會影響 minimization 同之後嘅 BDD", font_size=26, color=GREY_A, english_terms=["minimization", "BDD"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        points.next_to(takeaway, DOWN, buff=0.5)

        next_episode = mixed_text(
            "下集會正式進入 Binary Decision Diagram。",
            font_size=22,
            color=BLUE_B,
            english_terms=["Binary Decision Diagram"],
        )
        next_episode.next_to(points, DOWN, buff=0.48)

        self.play(Write(takeaway), run_time=1.0)
        elapsed += 1.0
        self.play(LaggedStart(*[FadeIn(point, shift=UP * 0.14) for point in points], lag_ratio=0.15), run_time=1.2)
        elapsed += 1.2
        self.play(FadeIn(next_episode, shift=UP * 0.12), run_time=0.8)
        elapsed += 0.8
        self.wait(1.0)
        elapsed += 1.0
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(VGroup(takeaway, points, next_episode, self.title_group)), run_time=0.9)
