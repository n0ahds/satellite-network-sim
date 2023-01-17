from spaceman3D.Orbit import Orbital
import spaceman3D.Orbit.astronomical_objects as a
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from mpl_toolkits.mplot3d import Axes3D
from mpltools import layout
import numpy as np

class Draw(object):

    def __init__(self):
        return

    fig = plt.figure(figsize=layout.figaspect(1))
    ax = fig.add_subplot(111, projection='3d')

    def plot_earth(self,radius):
        '''This function plots a celestial body at the origin of the plot.
        :param radius: Takes the radius of a celestial body
        :returns: angular coordinates
        '''

        coefs = (1, 1, 1)
        rx, ry, rz = [radius/np.sqrt(coef) for coef in coefs]

        # Azimuth Angle & Altitude in Spherical Coordinates
        phi = np.linspace(0, 2*np.pi, 100)
        theta = np.linspace(0, np.pi, 100)

        # Spherical Angles
        x = rx * np.outer(np.cos(phi), np.sin(theta))
        y = ry * np.outer(np.sin(phi), np.sin(theta))
        z = rz * np.outer(np.ones_like(phi), np.cos(theta))
        return x,y,z

    def orientation(self, inclination=0, right_ascension=0, argument_periapsis=0):
        '''This function defines the rotational matricies used to orient the ellipse.'''
        i = Orbital().degree_to_radian(inclination)
        R = np.matrix([[1, 0, 0],
                       [0, np.cos(i), -np.sin(i)],
                       [0, np.sin(i), np.cos(i)]])

        w_omega = Orbital().degree_to_radian(right_ascension)
        R2 = np.matrix([[np.cos(w_omega), -np.sin(w_omega), 0],
                        [np.sin(w_omega), np.cos(w_omega), 0],
                        [0, 0, 1]])

        omega = Orbital().degree_to_radian(argument_periapsis)
        R3 = np.matrix([[np.cos(omega), -np.sin(omega), 0],
                        [np.sin(omega), np.cos(omega), 0],
                        [0, 0, 1]])
        return R, R2, R3

    def polar_equation_of_ellipse(self,semi_major_axis,eccentricity,theta):
        '''This function defines the polar equation of an ellipse, and returns the radius, and polar coordinates.'''
        r = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*np.cos(theta))
        polar_x = r*np.cos(theta)
        polar_y = r*np.sin(theta)
        polar_z = 0*theta
        return r, polar_x, polar_y, polar_z

    def define_orbit(self,semi_major_axis=0, eccentricity=0, inclination=0,
                    right_ascension=0, argument_periapsis=0,theta=0,define_orbit=True):
        '''This function takes the orbital elements and uses them to define the Elliptical orbit in 3-Dimensions'''
        R, R2, R3 = self.orientation(inclination,right_ascension,argument_periapsis)
        r, polar_x, polar_y, polar_z = self.polar_equation_of_ellipse(semi_major_axis,eccentricity,theta)
        if define_orbit is True:
            points = np.matrix(list(zip(polar_x,polar_y,polar_z)))
        else:
            points = np.matrix([polar_x,polar_y,polar_z])
        pts =  (R * R2 * R3 * points.T)
        return pts

    def plot_orbit(self,semi_major_axis=0, eccentricity=0, inclination=0,right_ascension=0, argument_periapsis=0,
                    true_anomaly=0, label=None, object=None):
        "Draws orbit around an earth in units of kilometers."

        #Plot Earth
        x,y,z = self.plot_earth(radius=a.objects[str(object)]['radius'])
        self.ax.plot_surface(x, y, z, rstride=4, cstride=4, alpha=0.4, color=a.objects[str(object)]['color'])
        self.ax.set_axis_off()

        #Plot Orbit
        theta = np.linspace(0,2*np.pi,360)
        pts = self.define_orbit(semi_major_axis, eccentricity, inclination, right_ascension, argument_periapsis, theta)
        orbit_pts = pts.T
        xr,yr,zr = orbit_pts[:,0].A.flatten(), orbit_pts[:,1].A.flatten(), orbit_pts[:,2].A.flatten()
        self.ax.plot(xr, yr, zr, color='g', linestyle='-')

        # Plot Satellite
        sat_angle = Orbital().degree_to_radian(true_anomaly)
        sat = self.define_orbit(semi_major_axis,eccentricity,inclination,right_ascension,argument_periapsis,sat_angle,define_orbit=False)
        sat = sat.flatten()
        satx, saty, satz = sat[0,0], sat[0,1], sat[0,2]
        self.ax.plot([0, satx], [0, saty], [0, satz], 'b-')
        self.ax.plot([satx],[saty],[satz], 'bo')

        #Create X-axis Marker
        self.ax.plot([0,7500],[0,0],[0,0],'r:')
        self.ax.plot([7500],[0],[0],'r<')
        self.ax.text(7510,0,0,s='X', fontsize=10,color='w')

        #Create Y-axis Marker
        self.ax.plot([0,0],[0,7500],[0,0],'r:')
        self.ax.plot([0],[7500],[0],'r<')
        self.ax.text(0,7510,0,s='Y',fontsize=10,color='w')

        #Create Z-axis Marker
        self.ax.plot([0,0],[0,0],[0,7500],'r:')
        self.ax.plot([0],[0],[7500],'r^')
        self.ax.text(0,0,7510,s='Z', fontsize=10,color='w')

        #Create Z-axis Marker
        self.ax.plot([0,0],[0,0],[0,7500],'m-')
        self.ax.plot([0],[0],[7500],'m<')
        self.ax.text(0,0,7510,s='axis', fontsize=10,color='w')

        # Write satellite name next to it
        if label is not None:
            self.ax.text(satx, saty, satz, label, fontsize=11)

        #radius = np.sqrt(satx**2 + saty**2 + satz**2)
        #polar = np.arccos(satz/radius)
        #lon = o.degree_to_radian(polar-90)
        #lat = o.degree_to_radian(np.arctan2(saty, satx))

        #Lat = o.radian_to_degree(lat)
        #Lon = o.radian_to_degree(lon)
        #print("----------------------------------------------------------------------------------------")
        #print("{} : Projected Lat: {}° Long: {}°".format(label, Lat, Lon))

    def draw_orbit(self, *argv, object):
        '''This function calls the plot orbit function using the TLE elements defined in orbit.py'''
        o=Orbital()
        semi_major_axes = []
        for arg in argv:
            o.import_tle(tle=arg)
            semi_major_axis = o.semi_major_axis_calc()
            semi_major_axes.append(semi_major_axis)
            true_anomaly = o.anomoly_calc()
            self.plot_orbit(semi_major_axis, o.eccentricity, o.inclination, o.right_ascension,
                            o.argument_periapsis,true_anomaly, o.title, object=object)
        max_axis = max(semi_major_axes)
        self.ax.auto_scale_xyz([-max_axis,max_axis],[-max_axis,max_axis],[-max_axis,max_axis])
        plt.show()
