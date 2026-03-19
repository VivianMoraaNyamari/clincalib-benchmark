# ClinCalib: Clinical Confidence Calibration Benchmark

> **Metacognition Track — Kaggle Measuring AGI: Cognitive Abilities 2026**  
> Built by [@msnyamari](https://kaggle.com/msnyamari)

---

## What is ClinCalib?

ClinCalib evaluates **AI metacognition** — whether a model knows what it knows and what it doesn't — using clinical medicine as the evaluation domain.

Standard medical AI benchmarks (MedQA, MedMCQA) report accuracy alone. A model that answers a difficult clinical question with 95% confidence while being correct only 52% of the time is more dangerous in deployment than one that correctly says *"I am uncertain."* ClinCalib measures this gap directly.

---

## Three Tasks

| Task | Abbreviation | Cases | Primary Metric |
|------|-------------|-------|---------------|
| Confidence-Accuracy Calibration | CAC | 120 vignettes | Expected Calibration Error (ECE) |
| Uncertainty Flagging | UF | 80 cases | Sensitivity + Specificity |
| Error Detection & Self-Correction | EDC | 60 cases | Correction rate / Confabulation rate |

**Total: 260 evaluation items** across 6 clinical specialties.

---

## Task Descriptions

### Task 1 — Confidence-Accuracy Calibration (CAC)

The model states a confidence percentage (0–100%) **before** selecting a diagnosis from four options. This elicitation precedes the answer to prevent post-hoc rationalization.

Cases are stratified across three difficulty tiers:
- **Tier 1** — Textbook presentations (pancreatitis, uncomplicated UTI, acute stroke)
- **Tier 2** — Atypical presentations (silent MI in elderly diabetic, Kawasaki disease)
- **Tier 3** — Genuinely ambiguous (UCTD vs SLE, post-COVID vs ME/CFS, end-of-life capacity)

**Metrics:** Expected Calibration Error (ECE), Brier Score

### Task 2 — Uncertainty Flagging (UF)

The model chooses `DIAGNOSE` or `FLAG_UNCERTAINTY` for each case. Half the cases are solvable; half are deliberately underdetermined (missing history, investigations, or examination findings).

**Metrics:** Sensitivity and Specificity of uncertainty flagging, F1

### Task 3 — Error Detection & Self-Correction (EDC)

Two-turn interaction: the model answers a clinical question, receives a correction probe if an error is detected, then must revise. Tracks whether the model corrects itself or confabulates a justification.

**Metrics:** Correction rate, Confabulation rate, Regression rate

---

## Repository Structure

```
clincalib-benchmark/
│
├── README.md                        # This file
├── clincalib_benchmark.py           # Full benchmark code (kaggle-benchmarks SDK)
├── requirements.txt                 # Dependencies
│
└── data/
    ├── cac_cases.json               # 120 CAC vignettes with tiers and answers
    ├── uf_cases.json                # 80 UF cases (solvable + underdetermined)
    └── edc_cases.json               # 60 EDC cases with error signals
```

---

## Quickstart

### Install dependencies

```bash
pip install kaggle-benchmarks
```

### Run the benchmark

```bash
python clincalib_benchmark.py
```

### Or run via Kaggle Benchmarks SDK

```python
import kaggle_benchmarks as kbench

# Tasks are pre-registered on Kaggle Benchmarks
# kaggle.com/benchmarks/msnyamari/clincalib
```

---

## Dataset

All clinical vignettes are **original**, authored by a qualified clinical medicine practitioner. Ground truth is derived from:

- [NICE Clinical Guidelines](https://www.nice.org.uk/guidance)
- [WHO ICD-11](https://icd.who.int/)
- UpToDate clinical references

Cases cover: internal medicine, emergency medicine, paediatrics, obstetrics & gynaecology, surgery, and psychiatry.

No patient-identifiable information is present — all vignettes are synthetic.

---

## Key Finding

> A frontier model scored **93% accuracy on Tier 1** while stating ≥90% confidence on 87% of those cases — appearing well-calibrated. On Tier 3 (ambiguous cases) it stated **≥80% confidence while correct only 54% of the time** (ECE 0.27). Standard benchmarks report one accuracy number and miss this entirely.

---

## Metrics Explained

### Expected Calibration Error (ECE)

ECE measures how well stated confidence correlates with actual accuracy across confidence bins.

```
ECE = Σ (|bin| / N) × |avg_confidence - avg_accuracy|
```

- **ECE = 0.0** → perfect calibration
- **ECE > 0.2** → poor calibration (dangerous in high-stakes deployment)

### Brier Score

Mean squared error between confidence (as probability) and binary correctness.

```
Brier = (1/N) Σ (confidence_i - correct_i)²
```

Lower is better. Range: 0.0 (perfect) to 1.0 (worst).

---

## Pilot Results

| Model | Tier 1 ECE | Tier 2 ECE | Tier 3 ECE | Confabulation Rate |
|-------|-----------|-----------|-----------|-------------------|
| Frontier Model A | 0.09 | 0.18 | 0.27 | 34% |
| Open-source Model B | 0.14 | 0.23 | 0.34 | 38% |

*Pilot on 30 CAC cases and 6 EDC cases.*

---

## Kaggle Benchmark

Live benchmark: [kaggle.com/benchmarks/msnyamari/clincalib](https://kaggle.com/benchmarks/msnyamari/clincalib)

Kaggle competition: [kaggle.com/competitions/kaggle-measuring-agi](https://kaggle.com/competitions/kaggle-measuring-agi)

---

## Author

**Viviannyamari**  
Diploma in Clinical Medicine · BSc Applied Statistics with Computing · Incoming MSc Data Science and Analytics

---

## License

Released under **CC0 1.0 Universal** (Public Domain) in accordance with Kaggle competition rules.

---

## References

1. Guo et al. (2017). On calibration of modern neural networks. *ICML 2017*. https://arxiv.org/abs/1706.04599
2. Jin et al. (2021). What disease does this patient have? *Applied Sciences*, 11(14), 6421.
3. Kadavath et al. (2022). Language models (mostly) know what they know. https://arxiv.org/abs/2207.05221
4. Xiong et al. (2024). Can LLMs express their uncertainty? *ICLR 2024*. https://arxiv.org/abs/2306.13063
5. Brier, G.W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3.
6. WHO (2022). ICD-11. https://icd.who.int/
7. NICE (2023). Hypertension in adults: NG136. https://www.nice.org.uk/guidance/ng136
