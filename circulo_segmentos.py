from manim import *
import itertools as it
class CircleSegmentScene(Scene):
    CONFIG={
    'center':ORIGIN,
    'color_letters':[RED,BLUE,YELLOW,GREEN],
    'radius':2.5,
    }
    def construct(self):
        self.add_title()
        circle=self.add_circle()
        dots=self.choose_three_random_points()
        self.play(Create(circle))
        self.play(DrawBorderThenFill(dots))
        self.wait()
    def add_title(self):
        title=Text('Caso en dos dimensiones')
        color_letter=it.cycle(self.CONFIG['color_letters'])
        for letter in title.family_members_with_points():
            letter.set_color(next(color_letter))
        title.to_edge(UP,buff=.4)
        self.play(Write(title))
    def add_circle(self):
        circle=Circle(radius=self.CONFIG['radius'],color=BLUE_D,stroke_width=2)
        center=Dot().move_to(circle.get_center()).set_z_index(10)
        radius=Line(circle.get_center(),circle.points[0])
        circle.add(center,radius)
        return circle
    def choose_three_random_points(self):
        points=np.array([
            self.CONFIG['center']+rotate_vector(
                self.CONFIG['radius']*RIGHT,theta
            )
            for theta in np.random.random(size=3)*2*PI
        ])
        points_mob=self.points_mob=VGroup(*[
            Dot().move_to(point) for point in points
        ])
        points_label=VGroup(*[
            MathTex('p_%d' %(i+1))for i in range(len(points_mob))
        ])
        for label,mob in zip(points_label, points_mob):
            label.move_to(mob)
            vect=mob.get_center()
            vect/=np.linalg.norm(vect)
            label.shift(vect*.4)
            mob.add(label)
        return points_mob
    def add_lines(self):
        dots=self.points_mob