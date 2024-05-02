from jax0planet.oblate import OblateSystem, OblateBody, OblateTransitOrbit
from jax0planet.light_curve import oblate_lightcurve, legacy_oblate_lightcurve

from jaxoplanet.light_curves import limb_dark_light_curve
from jaxoplanet.orbits import TransitOrbit
import jax
import jax.numpy as jnp
from zodiax import filter_jit

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

oblate_lightcurve = jax.jit(legacy_oblate_lightcurve)

params = {'period':300.456,
          'radius':0.1,
          'u':jnp.array([0.3,0.2]),
          'f':0.1,
          'bo':0.8,
          'duration':0.4,
          'theta':0.0
}

orbit = TransitOrbit(
    period=params['period'], time_transit=0., duration=params['duration'], impact_param=params['bo'], radius=params['radius']
)

# Create the main window
root = tk.Tk()
root.wm_title("Oblate Lightcurve Plotter")
root.geometry('1200x800')


# Create a Figure and a Canvas to draw on
fig, (ax0, ax1) = plt.subplots(2,1, figsize=(5, 2), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a subplot to draw on

# Draw the initial light curves
t = jnp.linspace(-0.3, 0.3, 200)
lc = jax.vmap(limb_dark_light_curve(orbit, params['u']))(t)
oblate_lc = oblate_lightcurve(params, t)
ax0.plot(t, oblate_lc, label='oblate_lightcurve')
ax1.plot(t, (oblate_lc-lc-1)*1e6, label='oblate - circular')
ax0.set_xlabel('Time')
ax0.set_ylabel('Flux')
ax1.set_ylabel('Residual (ppm)')
# Update function
def update(val):
    params['theta'] = s_theta.get()
    params['bo'] = s_impact.get()
    params['radius'] = s_radius.get()
    params['f'] = s_f.get()
    orbit = TransitOrbit(
        period=params['period'], time_transit=0, duration=params['duration'], impact_param=params['bo'], radius=params['radius']
    )
    lc = jax.vmap(limb_dark_light_curve(orbit, params['u']))(t)
    oblate_lc = oblate_lightcurve(params, t=t)
    ax0.cla()
    ax1.cla()
    ax0.plot(t, oblate_lc, label='oblate_lightcurve')
    ax1.plot(t, (oblate_lc-lc-1)*1e6, label='oblate - circular')
    fig.canvas.draw_idle()

# Start the main loop

# Create sliders
s_theta = tk.Scale(root, label='Theta', from_=0.0, to=jnp.pi, orient=tk.HORIZONTAL, command=update,resolution=0.1, length=500)
s_impact = tk.Scale(root, label='Impact Param', from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=update,resolution=0.01, length=500)
s_radius = tk.Scale(root, label='Radius', from_=0.01, to=1.0, orient=tk.HORIZONTAL, command=update, resolution=0.01,  length=500)
s_f = tk.Scale(root, label='f', from_=0.0, to=0.5, orient=tk.HORIZONTAL, command=update, resolution=0.01, length=500)

s_theta.set(params['theta'])
s_impact.set(params['bo'])
s_radius.set(params['radius'])
s_f.set(params['f'])

s_theta.pack()
s_impact.pack()
s_radius.pack()
s_f.pack()

root.mainloop()