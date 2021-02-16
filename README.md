# Evaluating Lightness Models

Roadmap:
- [x] Create inventory
- [ ] Create background overview for onboarding of new assistant
  - [ ] Necessary background information and terminology
  - [ ] Accurate inventory (including where everything lives)
  - [ ] Background readings (?)
  - [ ] Goals & tasks
- [ ] Decide on minimal viable product
  - [ ] Overview with just models and illusions that we already have code for
  - [ ] Translate existing Matlab implementations to Python
  - [ ] (Unit)tests
  - [ ] Metrics ?
- [ ] Create a brain-score-org like interface (www.brain-score.org)

How to read the inventory:
We have an implementation for this in Python
We have an implementation for this in Matlab
We do not have an implementation for this

Models
- [X] ODOG (B&M 1997, 1999, 2015)
- [X] LODOG (RHS, 2007)
- [X] FLODOG (RHS, 2007)
- [X] Domijan’s filling-in model (Domijan, 2015)
- [ ] BIWAM (Otazu, Vanrell, & Parraga, 2008)
- [ ] Dakin & Bex model (Dakin & Bex, 2003)
- [ ] Francis filling-in model (Francis & Kim, 2012; Francis, 2015)
- [ ] Rudd model (Rudd 2001; Rudd & Zemach 2007; Zemach & Rudd 2007; Rudd 2013; ...)
- [ ] Richard Murray (Murray, 2018; Murray 2020)
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
- Sign / direction of effect
- How to quantify target brightness, from model output image
- Blakeslee & McCourt's way of estimating target brightness (spatial average ?)
- Robinson, Hammon & de Sa way of estimating target brightness (target meridian ? )
- Some filling-in algorithm to fill-in target region brightness estimate ?


Tasks
- Brightness estimation
- Brightness estimation in (narrowband) noise (see Betz, Shapley, Wichmann, & Maertens, 2015; Salmela & Laurinen, 2009)
- Brightness estimation after contour adaptation (Anstis & Greenlee, 2013; Anstis, 2014)
- Brightness estimation after flicker adaptation (Robinson & de Sa, 2012; 2013)



