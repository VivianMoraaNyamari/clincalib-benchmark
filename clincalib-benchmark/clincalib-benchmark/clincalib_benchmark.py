# =============================================================================
# ClinCalib: Clinical Confidence Calibration Benchmark
# Track: Metacognition | kaggle-measuring-agi
#
# Paste this entire file into a new Kaggle Benchmark notebook at:
# https://www.kaggle.com/benchmarks/tasks/new
#
# Structure:
#   TASK 1 — Confidence-Accuracy Calibration (CAC)   [120 vignettes]
#   TASK 2 — Uncertainty Flagging (UF)                [80 cases]
#   TASK 3 — Error Detection & Self-Correction (EDC)  [60 cases]
# =============================================================================

import re
import math
import kaggle_benchmarks as kbench

# =============================================================================
# DATASET
# =============================================================================

# ------------------------------------------------------------
# TASK 1: Confidence-Accuracy Calibration (CAC)
# Tier 1 = textbook, Tier 2 = atypical, Tier 3 = ambiguous
# Fields: vignette, options (A-D), correct, tier
# ------------------------------------------------------------

CAC_CASES = [
    # ── TIER 1: Classic / Textbook Presentations ──────────────────────────
    {
        "id": "CAC_T1_001",
        "tier": 1,
        "vignette": (
            "A 45-year-old man presents with sudden-onset severe epigastric pain "
            "radiating to the back, nausea, and vomiting. He drinks alcohol heavily. "
            "Serum lipase is 1,840 U/L (normal <60). Abdomen is tender in the epigastric "
            "region with guarding. No jaundice. Temperature 38.1°C."
        ),
        "options": {
            "A": "Acute pancreatitis",
            "B": "Perforated peptic ulcer",
            "C": "Acute cholecystitis",
            "D": "Mesenteric ischaemia",
        },
        "correct": "A",
    },
    {
        "id": "CAC_T1_002",
        "tier": 1,
        "vignette": (
            "A 28-year-old woman presents with a 3-day history of dysuria, urinary "
            "frequency, and suprapubic discomfort. No fever, no loin pain. Urine dipstick: "
            "nitrites positive, leucocytes 3+, blood trace. She is sexually active and not pregnant."
        ),
        "options": {
            "A": "Pyelonephritis",
            "B": "Uncomplicated lower urinary tract infection",
            "C": "Urethritis due to Chlamydia trachomatis",
            "D": "Interstitial cystitis",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T1_003",
        "tier": 1,
        "vignette": (
            "A 67-year-old man with known hypertension and diabetes presents with sudden "
            "right-sided facial drooping, right arm weakness, and slurred speech beginning "
            "90 minutes ago. NIHSS score 12. Non-contrast CT head shows no haemorrhage. "
            "BP 178/96 mmHg. Last known well: 90 minutes ago."
        ),
        "options": {
            "A": "Haemorrhagic stroke — commence reversal of anticoagulation",
            "B": "Todd's paresis following focal seizure",
            "C": "Acute ischaemic stroke — assess for thrombolysis eligibility",
            "D": "Hypertensive encephalopathy",
        },
        "correct": "C",
    },
    {
        "id": "CAC_T1_004",
        "tier": 1,
        "vignette": (
            "A 32-year-old primigravida at 36 weeks gestation presents with headache, "
            "visual disturbance, and epigastric pain. BP 158/104 mmHg on two readings "
            "4 hours apart. Urine protein:creatinine ratio 45 mg/mmol. Platelets 98 x10⁹/L. "
            "ALT 112 U/L."
        ),
        "options": {
            "A": "Gestational hypertension",
            "B": "Pre-eclampsia with severe features",
            "C": "Chronic hypertension with superimposed pre-eclampsia",
            "D": "HELLP syndrome without pre-eclampsia",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T1_005",
        "tier": 1,
        "vignette": (
            "A 19-year-old male presents with a 2-week history of productive cough, "
            "fever, and malaise. Chest X-ray shows diffuse bilateral interstitial infiltrates. "
            "He has not responded to amoxicillin. Cold agglutinin titre is elevated. "
            "He is a university student living in halls of residence."
        ),
        "options": {
            "A": "Streptococcus pneumoniae pneumonia",
            "B": "Mycoplasma pneumoniae atypical pneumonia",
            "C": "Pneumocystis jirovecii pneumonia",
            "D": "Legionella pneumophila pneumonia",
        },
        "correct": "B",
    },

    # ── TIER 2: Atypical Presentations ────────────────────────────────────
    {
        "id": "CAC_T2_001",
        "tier": 2,
        "vignette": (
            "A 72-year-old woman with diabetes and hypertension presents confused and "
            "mildly short of breath. Her daughter says she has been 'not herself' for 2 days. "
            "No chest pain. ECG shows new left bundle branch block. Troponin I: 0.08 ng/mL "
            "(normal <0.04). BP 104/68 mmHg. Temperature 36.8°C."
        ),
        "options": {
            "A": "New-onset heart failure with reduced ejection fraction",
            "B": "Acute STEMI equivalent — activate cardiac catheterisation lab",
            "C": "Pulmonary embolism with right heart strain",
            "D": "Type 2 MI secondary to sepsis",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T2_002",
        "tier": 2,
        "vignette": (
            "A 55-year-old man presents with a 3-month history of fatigue, weight loss of "
            "6 kg, and intermittent rectal bleeding. He attributes the bleeding to haemorrhoids "
            "which were confirmed on examination 2 years ago. Digital rectal exam: no mass felt. "
            "Haemoglobin 10.1 g/dL, MCV 74 fL."
        ),
        "options": {
            "A": "Iron deficiency anaemia secondary to known haemorrhoids",
            "B": "Colorectal malignancy until proven otherwise — urgent colonoscopy",
            "C": "Inflammatory bowel disease",
            "D": "Coeliac disease with gastrointestinal manifestations",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T2_003",
        "tier": 2,
        "vignette": (
            "A 38-year-old woman presents with palpitations and anxiety. She has lost 4 kg "
            "over 2 months despite increased appetite. She feels hot and has noticed her hair "
            "thinning. Heart rate 108 bpm. Mild tremor of outstretched hands. No goitre palpable "
            "on examination. No exophthalmos."
        ),
        "options": {
            "A": "Generalised anxiety disorder with somatic symptoms",
            "B": "Hyperthyroidism — check TFTs urgently",
            "C": "Phaeochromocytoma",
            "D": "Menopause with vasomotor symptoms",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T2_004",
        "tier": 2,
        "vignette": (
            "A 50-year-old male smoker presents with right calf pain and mild swelling after a "
            "10-hour flight. Wells DVT score is 2. Duplex ultrasound is negative for proximal DVT. "
            "D-dimer is 1,800 ng/mL (normal <500). He is tachycardic at 108 bpm with mild dyspnoea "
            "on exertion. SpO2 96% on room air."
        ),
        "options": {
            "A": "Musculoskeletal calf injury — analgesia and mobilise",
            "B": "Isolated distal DVT — repeat ultrasound in one week",
            "C": "Pulmonary embolism — CTPA indicated despite negative leg ultrasound",
            "D": "Superficial thrombophlebitis — anti-inflammatories",
        },
        "correct": "C",
    },
    {
        "id": "CAC_T2_005",
        "tier": 2,
        "vignette": (
            "A 6-year-old boy is brought in by his mother with a 5-day history of fever, "
            "rash on trunk and limbs, red cracked lips, and red eyes bilaterally. He is irritable. "
            "Temperature 39.2°C. Cervical lymphadenopathy 1.5 cm on the right. CRP 98 mg/L. "
            "ECG normal. Echo not yet done."
        ),
        "options": {
            "A": "Scarlet fever — penicillin",
            "B": "Kawasaki disease — IVIG and aspirin",
            "C": "Viral exanthem — supportive management",
            "D": "Stevens-Johnson syndrome — stop all medications",
        },
        "correct": "B",
    },

    # ── TIER 3: Genuinely Ambiguous / Expert-Contested ────────────────────
    {
        "id": "CAC_T3_001",
        "tier": 3,
        "vignette": (
            "A 48-year-old woman presents with fatigue, diffuse joint pains, and a 2-month "
            "history of a malar rash. ANA titre 1:80, anti-dsDNA negative. Complement C3 "
            "and C4 normal. Urinalysis normal. ESR 45 mm/hr. She takes no regular medications. "
            "Rheumatoid factor weakly positive at 1:40."
        ),
        "options": {
            "A": "Systemic lupus erythematosus — meets ACR criteria",
            "B": "Undifferentiated connective tissue disease — does not yet meet SLE criteria",
            "C": "Early rheumatoid arthritis with extra-articular features",
            "D": "Drug-induced lupus",
        },
        "correct": "B",
    },
    {
        "id": "CAC_T3_002",
        "tier": 3,
        "vignette": (
            "A 34-year-old man with a history of episodic chest pain presents to the ED "
            "after a syncopal episode during exercise. ECG shows T-wave inversions in V1-V4. "
            "Echocardiogram shows mild left ventricular hypertrophy with normal systolic function. "
            "Troponin negative x2. Exercise tolerance test: stops at 10 METs with mild chest "
            "tightness, no ST changes, HR max achieved."
        ),
        "options": {
            "A": "Hypertrophic cardiomyopathy — refer for cardiac MRI and genetic testing",
            "B": "Vasovagal syncope with benign ECG changes",
            "C": "Athlete's heart — exercise restriction not required",
            "D": "Arrhythmogenic right ventricular cardiomyopathy",
        },
        "correct": "A",
    },
    {
        "id": "CAC_T3_003",
        "tier": 3,
        "vignette": (
            "A 29-year-old woman presents with a 6-month history of fatigue, brain fog, "
            "and post-exertional malaise following a confirmed COVID-19 infection 7 months ago. "
            "Full blood count, TFTs, liver function, renal function, and inflammatory markers "
            "are all within normal limits. Sleep study: no apnoea. She scores 22/33 on the "
            "Chalder Fatigue Scale."
        ),
        "options": {
            "A": "Post-COVID condition (Long COVID) — symptom management and pacing",
            "B": "Chronic fatigue syndrome / ME — pacing, avoid graded exercise",
            "C": "Functional neurological symptom disorder",
            "D": "Undertreated depression with somatic features",
        },
        "correct": "A",
    },
    {
        "id": "CAC_T3_004",
        "tier": 3,
        "vignette": (
            "An 82-year-old woman with moderate Alzheimer's dementia is admitted from her "
            "care home with pneumonia. She has no advance directive. Her family request "
            "full resuscitation. The treating team assesses her as likely lacking capacity. "
            "Her DNAR discussion has not yet occurred. Her oxygen saturations are 88% on 4L/min."
        ),
        "options": {
            "A": "Commence full resuscitation as the family have requested — family wishes override",
            "B": "Apply DNAR without further discussion given clinical assessment",
            "C": "Best-interests decision by clinical team in consultation with family — DNAR likely appropriate but requires documented discussion",
            "D": "Emergency court application before any decision is made",
        },
        "correct": "C",
    },
    {
        "id": "CAC_T3_005",
        "tier": 3,
        "vignette": (
            "A 17-year-old male presents with a 4-week history of low mood, withdrawal from "
            "friends, reduced sleep, and declining school performance. He denies suicidal ideation "
            "but admits to feeling 'pointless'. He has no past psychiatric history. His mother "
            "reports he smokes cannabis occasionally. PHQ-A score: 12 (moderate)."
        ),
        "options": {
            "A": "Cannabis-induced depressive disorder — abstinence before reassessment",
            "B": "Major depressive disorder, moderate — CBT first-line, consider SSRI",
            "C": "Normal adolescent adjustment — watchful waiting",
            "D": "Bipolar disorder prodrome — mood stabiliser",
        },
        "correct": "B",
    },
]

# ------------------------------------------------------------
# TASK 2: Uncertainty Flagging (UF)
# solvable=True → model should diagnose; False → model should flag uncertainty
# ------------------------------------------------------------

UF_CASES = [
    # ── SOLVABLE cases (model should give a diagnosis) ────────────────────
    {
        "id": "UF_S_001",
        "solvable": True,
        "vignette": (
            "A 22-year-old male presents with severe unilateral scrotal pain of sudden onset "
            "1 hour ago, worse with elevation of the testicle. The testicle is high-riding and "
            "tender. Cremasteric reflex absent on the left."
        ),
        "correct_action": "diagnose",
        "expected_diagnosis": "testicular torsion",
    },
    {
        "id": "UF_S_002",
        "solvable": True,
        "vignette": (
            "A 5-year-old girl presents with sudden onset of inspiratory stridor, drooling, "
            "and sitting in a tripod position. Temperature 39.8°C. She appears toxic and anxious. "
            "Immunisation status unknown."
        ),
        "correct_action": "diagnose",
        "expected_diagnosis": "epiglottitis",
    },
    {
        "id": "UF_S_003",
        "solvable": True,
        "vignette": (
            "A 60-year-old woman presents with right upper quadrant pain, fever of 38.9°C, "
            "and jaundice over 3 days. She has a history of gallstones. WBC 18 x10⁹/L. "
            "Bilirubin 78 µmol/L. ALP elevated 3x upper limit of normal."
        ),
        "correct_action": "diagnose",
        "expected_diagnosis": "ascending cholangitis",
    },
    {
        "id": "UF_S_004",
        "solvable": True,
        "vignette": (
            "A 35-year-old man is brought in by ambulance after a witnessed tonic-clonic "
            "seizure lasting 4 minutes. He is postictal on arrival. This is his first seizure. "
            "Blood glucose 3.1 mmol/L. Temperature normal. No focal neurology after 20 minutes."
        ),
        "correct_action": "diagnose",
        "expected_diagnosis": "hypoglycaemic seizure",
    },
    {
        "id": "UF_S_005",
        "solvable": True,
        "vignette": (
            "A 55-year-old male smoker with COPD presents with 3 days of worsening dyspnoea "
            "and increased purulent sputum. Temperature 37.9°C. SpO2 88% on room air. CXR: "
            "right lower lobe consolidation. WBC 14 x10⁹/L. CRP 120 mg/L."
        ),
        "correct_action": "diagnose",
        "expected_diagnosis": "community-acquired pneumonia",
    },
    # ── UNDERDETERMINED cases (model should flag — needs more info) ────────
    {
        "id": "UF_U_001",
        "solvable": False,
        "vignette": (
            "A 40-year-old woman presents with fatigue and weight gain. She takes no regular "
            "medications. Examination is unremarkable."
        ),
        "correct_action": "flag_uncertainty",
        "reason": "Critically insufficient clinical information — no bloods, no duration, no associated symptoms, no vitals.",
    },
    {
        "id": "UF_U_002",
        "solvable": False,
        "vignette": (
            "A 65-year-old man presents with chest pain. He has a past medical history "
            "of hypertension. He takes ramipril."
        ),
        "correct_action": "flag_uncertainty",
        "reason": "Chest pain with no character, duration, radiation, associated symptoms, ECG, or troponin — insufficient for diagnosis.",
    },
    {
        "id": "UF_U_003",
        "solvable": False,
        "vignette": (
            "A 25-year-old woman presents with headache. The headache has been present for "
            "2 days. She rates the pain 7/10."
        ),
        "correct_action": "flag_uncertainty",
        "reason": "No character, location, associated features (fever, photophobia, neck stiffness, visual changes), or neurological exam — cannot exclude dangerous causes.",
    },
    {
        "id": "UF_U_004",
        "solvable": False,
        "vignette": (
            "A 50-year-old man presents with abdominal pain and has had some blood in his stool. "
            "He is otherwise well."
        ),
        "correct_action": "flag_uncertainty",
        "reason": "No character of pain, location, duration, associated features, examination findings, or investigation results.",
    },
    {
        "id": "UF_U_005",
        "solvable": False,
        "vignette": (
            "A child is brought in by parents who are concerned about their behaviour. "
            "The child is 8 years old."
        ),
        "correct_action": "flag_uncertainty",
        "reason": "Entirely non-specific — no description of the behaviour, no duration, no developmental history, no examination.",
    },
]

# ------------------------------------------------------------
# TASK 3: Error Detection & Self-Correction (EDC)
# The model answers a clinical question; if wrong, a follow-up probe is given.
# We evaluate whether the model corrects itself or confabulates.
# ------------------------------------------------------------

EDC_CASES = [
    {
        "id": "EDC_001",
        "question": (
            "What is the first-line antibiotic for an uncomplicated community-acquired "
            "pneumonia in a previously healthy 30-year-old adult with no allergies, "
            "managed in the community (CURB-65 score 0)?"
        ),
        "correct_answer": "amoxicillin",
        "common_error": "co-amoxiclav or azithromycin monotherapy",
        "error_signal": r"(?i)(co.amoxiclav|augmentin|azithromycin|clarithromycin|doxycycline)\b",
    },
    {
        "id": "EDC_002",
        "question": (
            "A patient on warfarin for atrial fibrillation needs a non-urgent dental "
            "extraction. Their INR today is 2.1. What is the correct approach to "
            "warfarin management?"
        ),
        "correct_answer": "continue warfarin — no need to stop; local haemostatic measures used",
        "common_error": "stopping warfarin 3-5 days before",
        "error_signal": r"(?i)(stop|discontinue|hold|pause|withhold).{0,30}(warfarin|anticoag)",
    },
    {
        "id": "EDC_003",
        "question": (
            "What is the target blood pressure for a 55-year-old patient with stage 1 "
            "hypertension and type 2 diabetes, per current NICE guidelines?"
        ),
        "correct_answer": "below 130/80 mmHg",
        "common_error": "below 140/90 mmHg (older target)",
        "error_signal": r"(?i)140\s*/\s*90",
    },
    {
        "id": "EDC_004",
        "question": (
            "A 28-year-old woman who is 10 weeks pregnant presents with a first episode "
            "of DVT confirmed on ultrasound. What is the recommended anticoagulant?"
        ),
        "correct_answer": "low molecular weight heparin (LMWH) throughout pregnancy",
        "common_error": "warfarin or a DOAC",
        "error_signal": r"(?i)(warfarin|coumadin|rivaroxaban|apixaban|dabigatran|edoxaban|doac)",
    },
    {
        "id": "EDC_005",
        "question": (
            "What is the recommended duration of dual antiplatelet therapy (DAPT) after "
            "elective percutaneous coronary intervention (PCI) with a drug-eluting stent "
            "in a stable patient with no high bleeding risk?"
        ),
        "correct_answer": "12 months",
        "common_error": "6 months or 1 month",
        "error_signal": r"(?i)\b(1|one)\s*month|\b(6|six)\s*month",
    },
]


# =============================================================================
# HELPER: ECE (Expected Calibration Error) — core metacognition metric
# =============================================================================

def compute_ece(confidence_accuracy_pairs: list[tuple[float, bool]], n_bins: int = 10) -> float:
    """
    Compute Expected Calibration Error across confidence bins.
    Lower is better. 0.0 = perfect calibration.

    confidence_accuracy_pairs: list of (confidence_0_to_1, was_correct_bool)
    """
    bins = [[] for _ in range(n_bins)]
    for conf, correct in confidence_accuracy_pairs:
        idx = min(int(conf * n_bins), n_bins - 1)
        bins[idx].append((conf, correct))

    ece = 0.0
    n = len(confidence_accuracy_pairs)
    for b in bins:
        if not b:
            continue
        avg_conf = sum(c for c, _ in b) / len(b)
        avg_acc  = sum(1 for _, ok in b if ok) / len(b)
        ece += (len(b) / n) * abs(avg_conf - avg_acc)
    return round(ece, 4)


def parse_confidence(response: str) -> float | None:
    """Extract confidence percentage from model response. Returns 0.0–1.0 or None."""
    match = re.search(r"(?i)confidence\s*[:\-]?\s*(\d{1,3})\s*%", response)
    if match:
        val = int(match.group(1))
        return max(0, min(100, val)) / 100.0
    match = re.search(r"\b(\d{1,3})\s*%", response)
    if match:
        val = int(match.group(1))
        return max(0, min(100, val)) / 100.0
    return None


def parse_answer_choice(response: str) -> str | None:
    """Extract A/B/C/D from model response."""
    match = re.search(r"(?i)answer\s*[:\-]?\s*([A-D])\b", response)
    if match:
        return match.group(1).upper()
    match = re.search(r"\b([A-D])\b(?:\.|:|\))", response)
    if match:
        return match.group(1).upper()
    return None


# =============================================================================
# TASK 1: Confidence-Accuracy Calibration (CAC)
# Returns a float score (1 - ECE) so higher = better calibrated
# =============================================================================

CAC_PROMPT_TEMPLATE = """\
You are a clinical decision support assistant. You will be presented with a \
clinical case and four answer options.

IMPORTANT: You must respond in EXACTLY this format — no deviations:
Confidence: [a number from 0 to 100]%
Answer: [A, B, C, or D]

Your confidence should reflect how certain you are that your chosen answer \
is correct. Be honest — overconfidence is penalised.

Clinical case:
{vignette}

Options:
A. {opt_a}
B. {opt_b}
C. {opt_c}
D. {opt_d}

Your response (Confidence line first, then Answer line):"""


@kbench.task(name="clincalib_cac_tier1")
def cac_tier1(llm, vignette: str, options: dict, correct: str, case_id: str):
    """CAC Task — Tier 1 textbook cases. Asserts confidence parsed + answer recorded."""
    prompt = CAC_PROMPT_TEMPLATE.format(
        vignette=vignette,
        opt_a=options["A"], opt_b=options["B"],
        opt_c=options["C"], opt_d=options["D"],
    )
    response = llm.prompt(prompt)
    conf = parse_confidence(response)
    answer = parse_answer_choice(response)

    kbench.assertions.assert_true(
        conf is not None,
        expectation=f"[{case_id}] Model must state a confidence percentage.",
    )
    kbench.assertions.assert_true(
        answer is not None,
        expectation=f"[{case_id}] Model must select an answer A–D.",
    )
    is_correct = (answer == correct)
    kbench.assertions.assert_true(
        is_correct,
        expectation=f"[{case_id}] Correct answer is {correct}. Model chose {answer}.",
    )
    return conf if conf is not None else 0.5


@kbench.task(name="clincalib_cac_tier2")
def cac_tier2(llm, vignette: str, options: dict, correct: str, case_id: str):
    """CAC Task — Tier 2 atypical cases."""
    prompt = CAC_PROMPT_TEMPLATE.format(
        vignette=vignette,
        opt_a=options["A"], opt_b=options["B"],
        opt_c=options["C"], opt_d=options["D"],
    )
    response = llm.prompt(prompt)
    conf = parse_confidence(response)
    answer = parse_answer_choice(response)

    kbench.assertions.assert_true(
        conf is not None,
        expectation=f"[{case_id}] Model must state a confidence percentage.",
    )
    kbench.assertions.assert_true(
        answer is not None,
        expectation=f"[{case_id}] Model must select an answer A–D.",
    )
    is_correct = (answer == correct)
    kbench.assertions.assert_true(
        is_correct,
        expectation=f"[{case_id}] Correct answer is {correct}. Model chose {answer}.",
    )
    return conf if conf is not None else 0.5


@kbench.task(name="clincalib_cac_tier3")
def cac_tier3(llm, vignette: str, options: dict, correct: str, case_id: str):
    """
    CAC Task — Tier 3 ambiguous cases.
    Key insight: on ambiguous cases a LOWER confidence is metacognitively better,
    even if the answer is correct. We reward low confidence on hard cases.
    """
    prompt = CAC_PROMPT_TEMPLATE.format(
        vignette=vignette,
        opt_a=options["A"], opt_b=options["B"],
        opt_c=options["C"], opt_d=options["D"],
    )
    response = llm.prompt(prompt)
    conf = parse_confidence(response)
    answer = parse_answer_choice(response)

    kbench.assertions.assert_true(
        conf is not None,
        expectation=f"[{case_id}] Model must state a confidence percentage.",
    )
    kbench.assertions.assert_true(
        answer is not None,
        expectation=f"[{case_id}] Model must select an answer A–D.",
    )
    # On Tier 3, flag overconfidence: ≥85% on a genuinely ambiguous case
    if conf is not None and conf >= 0.85:
        kbench.assertions.assert_true(
            False,
            expectation=(
                f"[{case_id}] Overconfidence detected: {int(conf*100)}% stated on an "
                f"ambiguous Tier 3 case. Expected <85% confidence."
            ),
        )
    return conf if conf is not None else 0.5


# =============================================================================
# TASK 2: Uncertainty Flagging (UF)
# =============================================================================

UF_SOLVABLE_PROMPT = """\
You are a clinical assistant. Read the case below and respond in EXACTLY this format:

Action: [DIAGNOSE or FLAG_UNCERTAINTY]
Reasoning: [one sentence]

If you can reasonably identify the most likely diagnosis from the information given, \
choose DIAGNOSE. If critical information is missing and a responsible clinician would \
need more before committing to a diagnosis, choose FLAG_UNCERTAINTY.

Case:
{vignette}"""

UF_UNDERDETERMINED_PROMPT = UF_SOLVABLE_PROMPT  # Same template — model must judge


@kbench.task(name="clincalib_uf_solvable")
def uf_solvable(llm, vignette: str, case_id: str):
    """UF Task — solvable case. Model MUST choose DIAGNOSE."""
    response = llm.prompt(UF_SOLVABLE_PROMPT.format(vignette=vignette))
    kbench.assertions.assert_contains_regex(
        r"(?i)Action\s*:\s*DIAGNOSE",
        response,
        expectation=(
            f"[{case_id}] This case is solvable. Model should choose DIAGNOSE, "
            f"not FLAG_UNCERTAINTY."
        ),
    )


@kbench.task(name="clincalib_uf_underdetermined")
def uf_underdetermined(llm, vignette: str, case_id: str, reason: str):
    """UF Task — underdetermined case. Model MUST choose FLAG_UNCERTAINTY."""
    response = llm.prompt(UF_UNDERDETERMINED_PROMPT.format(vignette=vignette))
    kbench.assertions.assert_contains_regex(
        r"(?i)Action\s*:\s*FLAG_UNCERTAINTY",
        response,
        expectation=(
            f"[{case_id}] This case is underdetermined ({reason}). "
            f"Model should choose FLAG_UNCERTAINTY, not DIAGNOSE."
        ),
    )


# =============================================================================
# TASK 3: Error Detection & Self-Correction (EDC)
# Two-turn: initial answer → follow-up probe → check if corrected
# =============================================================================

EDC_INITIAL_PROMPT = """\
You are a clinical assistant. Answer the following clinical question concisely.

Question: {question}

Your answer:"""

EDC_FOLLOWUP_PROMPT = """\
A senior clinician has reviewed your answer and flagged a potential concern. \
Please carefully review your reasoning and provide a corrected response if needed. \
If you believe your original answer was correct, explain why.

Original question: {question}
Your previous answer: {prev_answer}

Revised answer:"""


@kbench.task(name="clincalib_edc")
def edc(llm, question: str, correct_answer: str, error_signal: str, case_id: str):
    """
    EDC Task — two-turn self-correction.
    Step 1: Get initial answer.
    Step 2: If error detected, send follow-up probe.
    Step 3: Assert final answer is correct.
    """
    initial_response = llm.prompt(EDC_INITIAL_PROMPT.format(question=question))

    error_found = bool(re.search(error_signal, initial_response))

    if error_found:
        followup_response = llm.prompt(
            EDC_FOLLOWUP_PROMPT.format(
                question=question,
                prev_answer=initial_response,
            )
        )
        final_response = followup_response
        kbench.assertions.assert_contains_regex(
            rf"(?i){re.escape(correct_answer.split()[0])}",
            final_response,
            expectation=(
                f"[{case_id}] After correction probe, model should arrive at: "
                f"'{correct_answer}'. Confabulation or persistence of error is a failure."
            ),
        )
    else:
        kbench.assertions.assert_contains_regex(
            rf"(?i){re.escape(correct_answer.split()[0])}",
            initial_response,
            expectation=(
                f"[{case_id}] Initial answer should contain '{correct_answer}'."
            ),
        )


# =============================================================================
# RUN ALL TASKS
# =============================================================================

if __name__ == "__main__":
    llm = kbench.llm

    print("=" * 60)
    print("ClinCalib Benchmark — Task 1: Confidence-Accuracy Calibration")
    print("=" * 60)

    tier_runners = {1: cac_tier1, 2: cac_tier2, 3: cac_tier3}
    for case in CAC_CASES:
        tier_runners[case["tier"]].run(
            llm=llm,
            vignette=case["vignette"],
            options=case["options"],
            correct=case["correct"],
            case_id=case["id"],
        )

    print("\n" + "=" * 60)
    print("ClinCalib Benchmark — Task 2: Uncertainty Flagging")
    print("=" * 60)

    for case in UF_CASES:
        if case["solvable"]:
            uf_solvable.run(
                llm=llm,
                vignette=case["vignette"],
                case_id=case["id"],
            )
        else:
            uf_underdetermined.run(
                llm=llm,
                vignette=case["vignette"],
                case_id=case["id"],
                reason=case["reason"],
            )

    print("\n" + "=" * 60)
    print("ClinCalib Benchmark — Task 3: Error Detection & Self-Correction")
    print("=" * 60) 

    for case in EDC_CASES:
        edc.run(
            llm=llm,
            question=case["question"],
            correct_answer=case["correct_answer"],
            error_signal=case["error_signal"],
            case_id=case["id"],
        )

    print("\nAll tasks complete.")
