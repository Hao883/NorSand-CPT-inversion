from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, NumberField, Section, Text
import plotly.graph_objects as go
import numpy as np
from viktor.views import (
    PlotlyResult,
    PlotlyView,
)


class Parametrization(ViktorParametrization):
    Section0 = Section('Welcome to the NorSand CPT inversion app!')
    Section0.Intro = Text(
            """
This is a NorSand CPT inversion tool based on Jefferies, M. and Been, K., 2015. Soil liquefaction: a critical state approach. CRC press.
        """
    , visible=True, flex=100)


    section1 = Section('NorSand parameters: case 1')
    section1.G = NumberField('G (MPa)', variant='slider', min=5, max=150,default = 50,description = "Maximum elastic shear modulus")
    section1.M = NumberField('M', variant='slider', min=1, max=1.5,default = 1.4,step=0.05, description = 'Critical state friction ratio')
    section1.N = NumberField('N', variant='slider', min=0.2, max=0.5,default = 0.3,step=0.1, description = 'Volumetric coupling coefficient')
    section1.H = NumberField('H', variant='slider', min=25, max=500,default = 200, description = 'Plastic hardening modulus')
    section1.λ = NumberField('λ', variant='slider', min=0.01, max=0.07,default = 0.03,step=0.01, description = 'Slope of CSL')
    section1.ν = NumberField('λ', variant='slider', min=0.1, max=0.3,default = 0.2,step=0.05, description = "Poisson's ratio")
    section1.p = NumberField('p (kPa)', variant='slider', min=100, max=800,default = 100,step=100, description = 'Mean effective stress')

    section2 = Section('NorSand parameters: case 2')
    section2.G = NumberField('G (MPa)', variant='slider', min=5, max=150,default = 50,description = "Maximum elastic shear modulus")
    section2.M = NumberField('M', variant='slider', min=1, max=1.5,default = 1.4,step=0.05, description = 'Critical state friction ratio')
    section2.N = NumberField('N', variant='slider', min=0.2, max=0.5,default = 0.3,step=0.1, description = 'Volumetric coupling coefficient')
    section2.H = NumberField('H', variant='slider', min=25, max=500,default = 200, description = 'Plastic hardening modulus')
    section2.λ = NumberField('λ', variant='slider', min=0.01, max=0.07,default = 0.03,step=0.01, description = 'Slope of CSL')
    section2.ν = NumberField('λ', variant='slider', min=0.1, max=0.3,default = 0.2,step=0.05, description = "Poisson's ratio")
    section2.p = NumberField('p (kPa)', variant='slider', min=100, max=800,default = 100,step=100, description = 'Mean effective stress')

class Controller(ViktorController):
    label = 'LSTM'
    parametrization = Parametrization
    @PlotlyView("NorSand CPT inversion", duration_guess=1)
    # @ImageView("Image View", duration_guess=1)
    def get_plotly_and_data_view(self, params, **kwargs):
        f1 = 3.79 + 1.12*np.log(params.section1.G*1000 / params.section1.p)
        f2 = 1 + 1.06*(params.section1.M-1.25)
        f3 = 1 - 0.30*(params.section1.N-0.2)
        f4 = (params.section1.H / 100)**0.326
        f5 =  1 - 1.55*(params.section1.λ-0.01)
        f6 = 1
        f7 = 1.04 + 0.46*np.log(params.section1.G*1000 / params.section1.p)
        f8 = 1 - 0.40*(params.section1.M - 1.25)
        f9 = 1 - 0.30*(params.section1.N - 0.2)
        f10 = (params.section1.H / 100)**0.15
        f11 = 1 - 2.21*(params.section1.λ - 0.01)
        f12 = 1

        k = (f1*f2*f3*f4*f5*f6)**1.45
        m = 1.45*f7*f8*f9*f10*f11*f12

        f1b = 3.79 + 1.12*np.log(params.section2.G*1000 / params.section2.p)
        f2b = 1 + 1.06*(params.section2.M-1.25)
        f3b = 1 - 0.30*(params.section2.N-0.2)
        f4b = (params.section2.H / 100)**0.326
        f5b =  1 - 1.55*(params.section2.λ-0.01)
        f6b = 1
        f7b = 1.04 + 0.46*np.log(params.section2.G*1000 / params.section2.p)
        f8b = 1 - 0.40*(params.section2.M - 1.25)
        f9b = 1 - 0.30*(params.section2.N - 0.2)
        f10b = (params.section2.H / 100)**0.15
        f11b = 1 - 2.21*(params.section2.λ - 0.01)
        f12b = 1

        kb = (f1b*f2b*f3b*f4b*f5b*f6b)**1.45
        mb = 1.45*f7b*f8b*f9b*f10b*f11b*f12b

        psi = np.linspace(-0.3, 0.3, 100)

        x_min = -0.3
        x_max = 0.3
        Q = k*np.exp(-m*psi)
        Qb = kb*np.exp(-mb*psi)



        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=psi,
            y= Q,
            mode='lines',
            line=dict(color='blue', width=2),
            name='Case1',
            # hovertemplate='Settlement %{y} mm<extra></extra>',
        ))
        fig.add_trace(go.Scatter(
            x=psi,
            y= Qb,
            mode='lines',
            line=dict(color='red', width=2),
            name='Case2',
            # hovertemplate='Settlement %{y} mm<extra></extra>',
        ))


        fig.update_layout(
            xaxis=dict(range=[x_min, x_max], constrain='domain', scaleratio=1,title="State parameter \u03A8"),
            yaxis=dict( scaleratio=1,title="Dimensionless CPT resistance",type='log', tickvals=[10, 50, 100, 1000],dtick=1),
            annotations = [
            dict(
                x=1,  # Adjust these values to place the annotation where you want
                y=1,  # Adjust these values to place the annotation where you want
                showarrow=False,
                text="NorSand CPT",
                xref="paper",
                yref="paper",
                font=dict(
                    size=12,
                    color='black'
                ),
                bordercolor='black',
                borderwidth=1,
                borderpad=4,
                bgcolor='white',
                opacity=0.8
            )
        ]
            )
        return PlotlyResult(fig.to_json())
