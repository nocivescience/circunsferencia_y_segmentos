from manim import *
import itertools as it
class CircleSegmentScene(Scene):
    CONFIG={
    'center':.6*DOWN,
    'color_letters':[RED,BLUE,YELLOW,GREEN],
    'radius':2.5,
    }
    def construct(self):
        self.add_title()
        circle=self.add_circle()
        dots=self.choose_three_random_points()
        lines=self.get_center_lines()
        self.play(Create(circle))
        self.play(DrawBorderThenFill(dots))
        self.play(FadeIn(lines))
        self.note_special_region()
        # self.fix_two_points_in_place()
        self.draw_lines_through_center()
        self.wait()
    def add_title(self):
        title=Text('Caso en dos dimensiones')
        color_letter=it.cycle(self.CONFIG['color_letters'])
        for letter in title.family_members_with_points():
            letter.set_color(next(color_letter))
        title.to_edge(UP,buff=.15)
        self.play(Write(title))
    def add_circle(self):
        circle=self.circle=Circle(radius=self.CONFIG['radius'],color=BLUE_D,stroke_width=2).move_to(self.CONFIG['center'])
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
        triangle=self.get_triangle()
        self.point_labels=self.get_labels_update(points_mob,points_label)
        self.triangle_update=self.get_triangle_update(points_mob,points_label)
        self.update_animations=[self.point_labels,self.triangle_update]
        for anim,mob in zip(self.update_animations,[points_label,self.triangle]):
            mob.add_updater(anim)
        for label,mob in zip(points_label, points_mob):
            label.move_to(mob)
            vect=mob.get_center()
            vect/=np.linalg.norm(vect)
            label.shift(vect*.4)
            mob.add(label)
        return points_mob
    def get_triangle(self):
        triangle=self.triangle=RegularPolygon(n=3)
        triangle.set_fill(
            WHITE,opacity=.4
        )
        return triangle
    def get_triangle_update(self,points_mob,triangle):
        def update_triangle(triangle):
            points=[pm.get_center() for pm in points_mob]
            triangle.set_points_ascorners(points)
            if self.point_container_center(points):
                triangle.set_color(BLUE_C,opacity=.3)
    def get_labels_update(self, points_mob,labels):
        def update_labels(labels):
            for point_mob, label in zip(points_mob,labels):
                label.move_to_(point_mob)
                vect=point_mob.get_center()-self.CONFIG['center']
                vect/=np.linalg(vect)
                label.shift(.4*vect)
            return labels
        return UpdateFromFunc(labels,update_labels)
    def get_center_lines(self):
        angles=self.get_points_mob_angles()
        lines=VGroup()
        for angle in angles[:2]:
            line=DashedLine(
                self.CONFIG['radius']*RIGHT,
                self.CONFIG['radius']*LEFT
            )
            line.rotate(angle)
            line.shift(self.CONFIG['center'])
            line.set_color(WHITE)
            lines.add(line)
        self.center_lines=lines
        return lines
    def get_points_mob_angles(self):
        points_mobs=self.points_mob
        points=[pm.get_center()-self.CONFIG['center'] for pm in points_mobs]
        return np.array(list(map(angle_of_vector,points)))
    def get_all_arcs(self):
        angles=self.get_points_mob_angles()
        all_arcs=VGroup()
        for da0, da1 in it.product(*[[0,PI]]*2):
            arc_angle=(angles[1]+da1)-(angles[0]+da0)
            arc_angle=(arc_angle+np.pi)%(2*np.pi)-np.pi
            arc=Arc(
                start_angle=angles[0]+da0,
                angle=arc_angle,
                radius=self.CONFIG['radius'],
                stroke_width=8,
            )
            arc.shift(self.CONFIG['center'])
            all_arcs.add(arc)
        all_arcs.set_color_by_gradient(
            RED,BLUE
        )
        self.all_arcs=all_arcs
        return all_arcs
    def note_special_region(self):
        angles=self.get_points_mob_angles()
        all_arcs=self.get_all_arcs()
        arc=all_arcs[-1]
        arc_lines=VGroup()
        for angle in angles[:2]:
            line=Line(LEFT,RIGHT).scale(SMALL_BUFF)
            line.shift(self.CONFIG['radius']*RIGHT)
            line.rotate(angle+np.pi)
            line.shift(self.CONFIG['center'])
            arc_lines.add(line)
        self.play(Create(arc_lines))
    def fix_two_points_in_place(self):
        push_pins=VGroup()
        for point_mob in self.points_mob[:-1]:
            push_pin = Dot()
            push_pin.set_height(0.1)
            push_pin.move_to(point_mob.get_center(), DOWN)
            line = Line(ORIGIN, UP)
            line.set_stroke(WHITE, 2)
            line.set_height(0.1)
            line.move_to(push_pin, UP)
            line.shift(0.3*SMALL_BUFF*(2*DOWN+LEFT))
            push_pin.add(line)
            push_pin.set_fill(LIGHT_GREY)
            push_pin.save_state()
            push_pin.shift(UP)
            push_pin.fade(1)
            push_pins.add(push_pin)
        self.play(LaggedStartMap(
             ApplyMethod,push_pins, lambda mob: (mob.restore,) #hay que poner la coma al fina obligatoriamente
        ))
    def draw_lines_through_center(self):
        for line in self.get_center_lines():
            self.play((Create(line)))
        self.play(DrawBorderThenFill(self.all_arcs),Animation(self.points_mob))
        self.remove(self.circle)
        self.play(self.all_arcs.animate.space_out_submobjects(1.4),
            Animation(self.points_mob),rate_func=there_and_back,run_time=2)
        self.change_points_mob([0,0,np.mean(self.get_points_mob_angles()[:2]) +np.pi-self.get_points_mob_angles()[2]])
    def point_container_center(self,points):
        p0,p1,p2=points
        V1=p1-p0
        V2=p2-p0
        c=self.CONIFG['center']-p0
        M=np.matrix([V1[:2],V2[:2]]).T
        M_inv=np.linalg.inv(M)
        coords=np.dot(M_inv,c)
        return np.all(coords>0) and (np.sum(coords.flatten())<=1)
    def get_point_mob_theta_change_anim(self,point_mob,d_theta):
        curr_theta=angle_of_vector(point_mob.get_center()-self.CONFIG['center'])
        d_theta=(d_theta+np.pi)%(2*np.pi)-np.pi
        new_theta=curr_theta-+d_theta
        def update_point(point_mob,alpha):
            theta=interpolate(curr_theta,new_theta,alpha)
            point_mob.move_to(
                self.CONFIG['center']+self.CONFIG['radius']*(
                    np.cos(theta)*RIGHT+np.sin(theta)*UP
                )
            )
            return point_mob
        return UpdateFromAlphaFunc(point_mob,update_point,run_time=2)
    def change_points_mob(self,d_theta,*added_anims,**kwargs):
        anims=it.chain(self.animations,[self.get_point_mob_theta_change_anim(pm,dt) for pm,dt in zip(
            self.points_mob,d_theta
        )],added_anims)
        self.play(*anims,**kwargs)