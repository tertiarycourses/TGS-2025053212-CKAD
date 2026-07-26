"""
CKAD Pipeline Runner
====================
Orchestrates: Audit → Fix → Re-audit loop until PASS or max iterations.

Usage:
    python run_pipeline.py <input.pptx> [--out <output.pptx>] [--max-iter 5]

Example:
    python run_pipeline.py courseware/CKAD_Domain5_patch.pptx --out courseware/CKAD_clean.pptx
"""
import sys, os, json, argparse, subprocess, shutil
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "audit_ckad.py")
FIX   = os.path.join(HERE, "fix_ckad.py")
PY    = sys.executable


def run_audit(pptx_path):
    result = subprocess.run(
        [PY, AUDIT, pptx_path],
        capture_output=True, text=True, encoding='utf-8'
    )
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  [AUDIT ERROR] Could not parse output:\n{result.stdout[:500]}")
        raise
    return report


def run_fix(pptx_path, report_path, out_path):
    result = subprocess.run(
        [PY, FIX, pptx_path, report_path, out_path],
        capture_output=False, text=True, encoding='utf-8'
    )
    return result.returncode == 0


def pipeline(input_path, output_path, max_iter=5):
    print(f"\n{'='*65}")
    print(f"CKAD PIPELINE: {os.path.basename(input_path)}")
    print(f"{'='*65}\n")

    current = input_path
    tmp_dir = os.path.join(HERE, "_tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    for iteration in range(1, max_iter + 1):
        print(f"── Iteration {iteration} ──────────────────────────────────────")

        # Audit
        print(f"  [AUDIT]  {os.path.basename(current)}")
        report = run_audit(current)
        n_viol = len(report["violations"])
        print(f"  Slides: {report['total_slides']}  Labs: {len(report['labs_found'])}  Violations: {n_viol}")

        if report["pass"]:
            print(f"\n  ✓ AUDIT PASS after {iteration-1} fix iteration(s)")
            break

        for v in report["violations"]:
            print(f"    • [{v['rule']}] slide {v['slide']}: {v.get('detail','')[:70]}")

        # Save report
        report_path = os.path.join(tmp_dir, f"report_iter{iteration}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        # Only auto-fixable violations?
        fixable = {"admin_slide", "missing_killercoda_url"}
        unfixable = [v for v in report["violations"] if v["rule"] not in fixable]

        # Fix
        fixed_path = os.path.join(tmp_dir, f"fixed_iter{iteration}.pptx")
        print(f"  [FIX]   → {os.path.basename(fixed_path)}")
        run_fix(current, report_path, fixed_path)

        if unfixable:
            print(f"\n  ⚠ {len(unfixable)} unfixable violation(s) — stopping loop:")
            for v in unfixable:
                print(f"    • [{v['rule']}] {v.get('detail','')}")
            current = fixed_path
            break

        current = fixed_path

    else:
        print(f"\n  ✗ AUDIT still failing after {max_iter} iterations — check manually")

    # Copy final result to output
    shutil.copy(current, output_path)
    print(f"\n{'='*65}")
    print(f"OUTPUT → {output_path}")

    # Final audit summary
    final = run_audit(output_path)
    status = "PASS ✓" if final["pass"] else "FAIL ✗"
    print(f"FINAL STATUS: {status}  ({final['total_slides']} slides, {len(final['labs_found'])} labs, {len(final['violations'])} violations)")
    print(f"{'='*65}\n")
    return final["pass"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input PPTX path")
    parser.add_argument("--out", help="Output PPTX path", default=None)
    parser.add_argument("--max-iter", type=int, default=5)
    args = parser.parse_args()

    base, ext = os.path.splitext(args.input)
    out = args.out or f"{base}_clean{ext}"

    ok = pipeline(args.input, out, args.max_iter)
    sys.exit(0 if ok else 1)
