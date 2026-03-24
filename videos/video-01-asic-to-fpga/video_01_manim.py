from pathlib import Path

from manim import *
from pydub import AudioSegment

SCRIPT_DIR = Path(__file__).resolve().parent

config.background_color = "#0B1020"
config.video_dir = str(SCRIPT_DIR)
config.partial_movie_dir = str(SCRIPT_DIR / "partial_movie_files" / "{quality}" / "{scene_name}")

ZH_FONT = "Noto Sans HK"
EN_FONT = "Tahoma"
AUDIO_DIR = SCRIPT_DIR / "audio"
COVER_PATH = SCRIPT_DIR / "bookcover.png"


def zh_text(content: str, font_size: int, color=WHITE) -> Text:
    return Text(content, font=ZH_FONT, font_size=font_size, color=color, disable_ligatures=True)


def en_text(content: str, font_size: int, color=WHITE) -> Text:
    return Text(content, font=EN_FONT, font_size=font_size, color=color, disable_ligatures=True)


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


def make_chip(title: str, subtitle: str, color: str) -> VGroup:
    body = RoundedRectangle(
        corner_radius=0.18,
        width=2.8,
        height=1.6,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=0.14,
    )
    name = en_text(title, font_size=34)
    subtitle_terms = [term for term in ["ASIC", "PLD", "FPGA", "SoC", "LUT-based"] if term in subtitle]
    note = mixed_text(subtitle, font_size=18, color=GREY_B, english_terms=subtitle_terms)
    labels = VGroup(name, note).arrange(DOWN, buff=0.12).move_to(body)
    return VGroup(body, labels)


def make_stage(title: str, color: str) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.15,
        width=2.7,
        height=1.15,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=0.14,
    )
    english_terms = [term for term in ["HDL", "Logic Synthesis", "Technology Mapping", "LUT Blocks"] if term in title]
    label = mixed_text(title, font_size=22, english_terms=english_terms).move_to(box)
    return VGroup(box, label)


class Video01AsicToFpga(Scene):
    def construct(self):
        self.show_book_intro()
        self.create_header()
        self.show_title()
        self.show_platforms()
        self.show_mapping_flow()
        self.show_fpga_view()
        self.show_takeaway()

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

        summary_title = zh_text("本書重點", font_size=28, color=GOLD_B)
        summary_line = mixed_text(
            "BDD  |  Decomposition  |  Technology Mapping  |  實驗比較",
            font_size=18,
            color=GREY_A,
            english_terms=["BDD", "Decomposition", "Technology Mapping"],
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

    def start_voiceover(self, filename: str) -> float:
        audio_path = AUDIO_DIR / filename
        self.add_sound(str(audio_path))
        return AudioSegment.from_file(audio_path).duration_seconds

    def finish_voiceover(self, duration: float, elapsed: float, padding: float = 0.2):
        remaining = duration - elapsed
        if remaining > 0:
            self.wait(remaining + padding)

    def show_title(self):
        voice_duration = self.start_voiceover("01_title.mp3")
        elapsed = 0.0

        title = zh_text("第 1 集", font_size=42, color=BLUE_B)
        subtitle = mixed_text("由 ASIC 到 FPGA", font_size=56, english_terms=["ASIC", "FPGA"])
        tagline = mixed_text("點解 Technology Mapping 咁重要？", font_size=28, color=GREY_B, english_terms=["Technology Mapping"])
        group = VGroup(title, subtitle, tagline).arrange(DOWN, buff=0.22)

        self.play(FadeIn(group, shift=UP), run_time=1.4)
        elapsed += 1.4
        self.wait(0.8)
        elapsed += 0.8
        self.play(group.animate.scale(0.72).to_edge(UP, buff=1.05), run_time=0.9)
        elapsed += 0.9
        self.finish_voiceover(voice_duration, elapsed)
        self.title_group = group

    def show_platforms(self):
        voice_duration = self.start_voiceover("02_platforms.mp3")
        elapsed = 0.0

        asic = make_chip("ASIC", "固定晶片", BLUE_D)
        pld = make_chip("PLD", "可編程邏輯", GREEN_D)
        fpga = make_chip("FPGA", "LUT-based 架構", GOLD_D)
        soc = make_chip("SoC", "系統級整合", PURPLE_D)

        chips = VGroup(asic, pld, fpga, soc).arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.45))
        chips.scale(0.92).move_to(DOWN * 0.2)

        self.play(
            LaggedStart(*[FadeIn(chip, shift=UP * 0.25) for chip in chips], lag_ratio=0.15),
            run_time=1.8,
        )
        elapsed += 1.8
        self.play(Indicate(fpga, color=YELLOW), run_time=1.0)
        elapsed += 1.0

        focus = mixed_text("FPGA 最大優勢係可以重複編程。", font_size=24, color=GREY_A, english_terms=["FPGA"])
        focus.next_to(chips, DOWN, buff=0.55)
        self.play(Write(focus), run_time=1.1)
        elapsed += 1.1
        self.wait(0.8)
        elapsed += 0.8
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(chips), FadeOut(focus), run_time=0.8)

    def show_mapping_flow(self):
        voice_duration = self.start_voiceover("03_mapping_flow.mp3")
        elapsed = 0.0

        hdl = make_stage("HDL 設計", BLUE_D)
        synth = make_stage("Logic Synthesis", TEAL_D)
        mapping = make_stage("Technology Mapping", GOLD_D)
        lut = make_stage("LUT Blocks", GREEN_D)

        flow = VGroup(hdl, synth, mapping, lut).arrange(RIGHT, buff=0.4).scale(0.8)
        flow.move_to(ORIGIN + DOWN * 0.2)

        arrows = VGroup(
            Arrow(hdl.get_right(), synth.get_left(), buff=0.15, stroke_width=4, color=GREY_B),
            Arrow(synth.get_right(), mapping.get_left(), buff=0.15, stroke_width=4, color=GREY_B),
            Arrow(mapping.get_right(), lut.get_left(), buff=0.15, stroke_width=4, color=GREY_B),
        )

        self.play(LaggedStart(*[FadeIn(stage, shift=UP * 0.2) for stage in flow], lag_ratio=0.1), run_time=1.4)
        elapsed += 1.4
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.12), run_time=1.2)
        elapsed += 1.2
        self.play(Indicate(mapping, color=YELLOW), run_time=0.9)
        elapsed += 0.9

        line_1 = mixed_text("硬件架構會影響 synthesis 同 mapping。", font_size=22, color=GREY_A, english_terms=["synthesis", "mapping"])
        line_2 = mixed_text("優秀 mapping 要善用有限 LUT 資源。", font_size=22, color=GREY_A, english_terms=["mapping", "LUT"])
        notes = VGroup(line_1, line_2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        notes.next_to(flow, DOWN, buff=0.7)

        self.play(FadeIn(notes, shift=UP * 0.2), run_time=1.0)
        elapsed += 1.0
        self.wait(0.9)
        elapsed += 0.9
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(flow), FadeOut(arrows), FadeOut(notes), run_time=0.8)

    def show_fpga_view(self):
        voice_duration = self.start_voiceover("04_fpga_view.mp3")
        elapsed = 0.0

        title = mixed_text("LUT-based FPGA 內部視角", font_size=32, color=BLUE_B, english_terms=["LUT-based", "FPGA"])
        title.next_to(self.title_group, DOWN, buff=0.4)

        grid = VGroup()
        for _ in range(12):
            cell = RoundedRectangle(
                corner_radius=0.08,
                width=1.18,
                height=0.72,
                stroke_color=BLUE_E,
                stroke_width=2,
                fill_color=BLUE_E,
                fill_opacity=0.22,
            )
            label = en_text("LUT", font_size=20)
            grid.add(VGroup(cell, label.move_to(cell)))

        grid.arrange_in_grid(rows=3, cols=4, buff=(0.25, 0.25)).move_to(LEFT * 1.4 + DOWN * 0.2)

        inputs = en_text("Boolean function", font_size=24, color=GREEN_B)
        inputs.move_to(RIGHT * 4 + UP * 1.5)
        arrow_in = Arrow(inputs.get_left(), grid.get_right() + UP * 0.25, buff=0.2, color=GREEN_B, stroke_width=4)

        metric_area = en_text("Area", font_size=26, color=YELLOW_B)
        metric_delay = en_text("Delay", font_size=26, color=RED_B)
        metric_route = en_text("Routing", font_size=26, color=TEAL_B)
        metrics = VGroup(metric_area, metric_delay, metric_route).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        metrics.move_to(RIGHT * 4 + DOWN * 0.6)

        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(grid, lag_ratio=0.05), run_time=1.4)
        elapsed += 1.4
        self.play(FadeIn(inputs), GrowArrow(arrow_in), run_time=0.9)
        elapsed += 0.9

        highlighted = [grid[1], grid[2], grid[5], grid[6]]
        self.play(
            *[cell[0].animate.set_fill(GOLD_D, opacity=0.45).set_stroke(GOLD_B, width=3) for cell in highlighted],
            run_time=1.0,
        )
        elapsed += 1.0
        self.play(FadeIn(metrics, shift=LEFT * 0.2), run_time=1.0)
        elapsed += 1.0
        self.wait(1.0)
        elapsed += 1.0
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(title), FadeOut(grid), FadeOut(inputs), FadeOut(arrow_in), FadeOut(metrics), run_time=0.8)

    def show_takeaway(self):
        voice_duration = self.start_voiceover("05_takeaway.mp3")
        elapsed = 0.0

        takeaway = mixed_text(
            "Technology Mapping 將抽象邏輯\n變成實際硬件配置",
            font_size=30,
            color=GOLD_B,
            english_terms=["Technology Mapping"],
        )
        takeaway.move_to(UP * 0.65)

        points = VGroup(
            mixed_text("善用 FPGA 架構", font_size=26, color=GREY_A, english_terms=["FPGA"]),
            mixed_text("將 function 高效放入 LUT", font_size=26, color=GREY_A, english_terms=["function", "LUT"]),
            mixed_text("降低 area、delay、routing 壓力", font_size=26, color=GREY_A, english_terms=["area", "delay", "routing"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        points.next_to(takeaway, DOWN, buff=0.55)

        self.play(Write(takeaway), run_time=1.1)
        elapsed += 1.1
        self.play(LaggedStart(*[FadeIn(point, shift=UP * 0.15) for point in points], lag_ratio=0.15), run_time=1.3)
        elapsed += 1.3
        self.wait(1.4)
        elapsed += 1.4
        self.finish_voiceover(voice_duration, elapsed)
        self.play(FadeOut(VGroup(takeaway, points, self.title_group)), run_time=0.9)
