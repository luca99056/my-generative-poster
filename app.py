import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st

PALETTE = ['#ef7fa8', '#73c7b0', '#f1c36d', '#8d79b7', '#7db4d8', '#e89a73']

def blob_points(cx, cy, radius, wobble=0.12, n=180, seed=0):
    r = np.random.default_rng(seed)
    a = np.linspace(0, 2*np.pi, n, endpoint=False)
    phase1, phase2 = r.uniform(0, 2*np.pi, 2)
    rr = radius * (1 + wobble * (0.55*np.sin(3*a+phase1)
          + 0.3*np.sin(5*a+phase2) + 0.15*r.normal(size=n)))
    return np.c_[cx + rr*np.cos(a), cy + rr*np.sin(a)]

def make_palette(mode, seed):
    if mode == 'Original':
        return PALETTE
    import colorsys
    rng = np.random.default_rng(seed)
    result = []
    base_hue = rng.random()
    for _ in range(6):
        if mode == 'Pastel':
            h, s, v = rng.random(), rng.uniform(.15,.35), rng.uniform(.9,1.)
        elif mode == 'Vivid':
            h, s, v = rng.random(), rng.uniform(.8,1.), rng.uniform(.8,1.)
        elif mode == 'Mono':
            h, s, v = base_hue, rng.uniform(.2,.6), rng.uniform(.5,1.)
        else:
            h, s, v = rng.random(), rng.uniform(.3,1.), rng.uniform(.5,1.)
        result.append(colorsys.hsv_to_rgb(h,s,v))
    return result

def render(layers=7, wobble=.13, palette_mode='Original', seed=42):
    fig, ax = plt.subplots(figsize=(6,8))
    fig.patch.set_facecolor('#f5f1e8')
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis('off')
    ax.set_facecolor('#f5f1e8')
    rng = np.random.default_rng(seed)
    palette = make_palette(palette_mode, seed)
    centers = [(0.22,0.28),(0.74,0.72),(0.66,0.30),(0.30,0.70)]
    for i in range(int(layers)):
        cx, cy = centers[i % len(centers)]
        cx += rng.normal(0,.045)
        cy += rng.normal(0,.045)
        radius = rng.uniform(.16,.29)
        pts = blob_points(cx, cy, radius, wobble, seed=seed+i)
        for d, alpha in [(.035,.08),(.022,.10),(.012,.13)]:
            ax.add_patch(Polygon(pts + [d,-d], closed=True,
                         facecolor='black', edgecolor='none', alpha=alpha))
        ax.add_patch(Polygon(pts, closed=True,
                     facecolor=palette[i % len(palette)], edgecolor='none', alpha=.78))
    ax.text(.06,.94,'GENERATIVE MOTION',fontsize=18,weight='bold',va='top')
    ax.text(.06,.905,'ART × DATA / WEEK 04',fontsize=8,va='top')
    return fig

st.set_page_config(page_title='Generative Motion', layout='centered')
st.title('GENERATIVE MOTION')
st.caption('Arts and Advanced Big Data | From Colab to the Web')
with st.sidebar:
    st.header('Poster controls')
    layers = st.slider('Layers', 3, 12, 7, 1)
    wobble = st.slider('Wobble', .03, .25, .13, .01)
    palette_mode = st.selectbox('Palette mode', ['Original','Pastel','Vivid','Mono','Random'])
    seed = st.slider('Seed', 0, 9999, 42, 1)
fig = render(layers, wobble, palette_mode, seed)
st.pyplot(fig, clear_figure=True)
plt.close(fig)
