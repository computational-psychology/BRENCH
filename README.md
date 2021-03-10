# Evaluating Lightness Models

Roadmap:
- [x] Create inventory
- [ ] Create background overview for onboarding of new assistant
  - [ ] Necessary background information and terminology
  - [ ] Accurate inventory (including where everything lives)
  - [ ] Background readings (?)
  - [ ] Goals & tasks
- [ ] Minimal viable product: pipeline to produce an overview
  - [ ] Models:
    - [ ] a (F)(L)ODOG model
    - [ ] a Domijan model
  - [ ] Stimuli:
    - [ ] a few that we currently have
  - [ ] Metric:
    - [ ] direction of effect for each Model x Stimulus combination
  - [ ] all with (Unit)tests
- Tasks:
  1. [ ] Pipeline
  1. [ ] Translate existing Matlab implementations to Python
- [ ] Create a brain-score-org like interface (www.brain-score.org)


Models
- [X] ODOG (B&M 1997, 1999, 2015)
- [X] LODOG (RHS, 2007)
- [X] FLODOG (RHS, 2007)
- [X] Domijan’s filling-in model (Domijan, 2015)
- [x] Francis filling-in model (Francis & Kim, 2012; Francis, 2015)
- [ ] BIWAM (Otazu, Vanrell, & Parraga, 2008; **MATLAB code**)
- [ ] Dakin & Bex model (Dakin & Bex, 2003; **MATLAB code**)
- [ ] Murray's probabilistic model (Murray, 2018; Murray 2020; **MATLAB code in Murray2020**)
- [ ] High-pass model (Shapiro & Lu, 2011; **MATLAB code in Murray2020**)
- [ ] Retinex model (Land & McCann, 1971; McCann, 1999; **MATLAB code in Murray2020**)
- [ ] Rudd model (Rudd 2001; Rudd & Zemach 2007; Zemach & Rudd 2007; Rudd 2013; ...)
- [ ] Grossberg and Todorovic filling-in model (Grossberg & Todorovic, 1988)


Phenomena / stimuli
- [X] Simultaneous Brightness Contrast (SBC)
- [X] White’s illusion
- [X] Anderson’s White’s illusion
- [X] Howe’s White’s illusion
- [X] Zigzag White’s illusion
- [X] Radial White’s illusion
- [X] Circular White’s illusion
- [X] Inverted White’s illusion
- [X] Grating induction
- [X] Todorovic’s SBC: equal
- [X] Todorovic’s SBC: in
- [X] Todorovic’s SBC: out
- [X] Checkerboard
- [X] Checkerboard extended
- [X] Mondrians
- [X] Benary’s cross
- [X] Todorovic’s Benary’s cross
- [X] Bullseye illusion
- [X] Dungeon illusion
- [X] Grating illusion
- [X] Ring illusion
- [X] Cube illusion
- [X] Contrast illusion
- [ ] Koffka illusion(s)
- [ ] Craig-O’Brien-Cornsweet illusion
- [ ] Assimilation (hsf gratings)
- [ ] Counterphase lightness induction
- [ ] Argyle
- [ ] Adelson (anti)snake


Parameterizations
- Parameterizations that (might) quantitatively change model prediction and psychophysical performance, e.g., carrier grating sf
- Parameterizations that (might) qualitatively change model prediction and perception, e.g., multiple targets that form an illusory surface
- Inventory could be used to identify parameterizations of stimuli for which models diverge

Metrics
- Sign / direction of effect (qualitative)
- Semi-quantitative comparisons for stimulus pairs ("Does the model predict a stronger brightness difference in stimulus X as compared to stimulus Y?", e.g. Murray2020)
- Testing the models on "control stimuli" that elicit no strong illusion in humans (e.g. connected Koffka-Ring, see Murray2020): the models should not predict large differences in these controls
- How to quantify target brightness, from model output image
- Blakeslee & McCourt's way of estimating target brightness (spatial average ?)
- Robinson, Hammon & de Sa way of estimating target brightness (target meridian ? )
- Some filling-in algorithm to fill-in target region brightness estimate ?

Tasks
- Brightness estimation
- Tests for glow, codetermination and articulation (see Murray2020)
- Brightness estimation in (narrowband) noise (see Betz, Shapley, Wichmann, & Maertens, 2015; Salmela & Laurinen, 2009)
- Brightness estimation after contour adaptation (Anstis & Greenlee, 2013; Anstis, 2014)
- Brightness estimation after flicker adaptation (Robinson & de Sa, 2012; 2013)
