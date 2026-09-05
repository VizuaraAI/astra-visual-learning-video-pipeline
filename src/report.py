"""Build the final report from completed media checks and measured worker records."""
from pathlib import Path
import argparse,json,datetime,shutil
ROOT=Path(__file__).resolve().parents[1]

def run(work,delivery):
    media=json.loads((delivery/'contact-sheets/media-verification.json').read_text())
    assert set(media)=={'cell','heart','dna'},'All three masters must be verified'
    assert all(all(v['checks'].values()) for v in media.values())
    totals={k:dict(estimated_usd=0.,worker_seconds=0.,completed_chunks=0,failed_attempts=0) for k in media}
    records=[];seen=set()
    folders={'bench-results':'bench','bench-gpu-results':'bench-gpu-denoise','bench-fallback-results':'bench-fallback','bench-prod-results':'bench-prod','bench-cpu-results':'bench-cpu','bench-cpu-cell-results':'bench-cpu-cell','probe-direct-results':'probe-direct','status':'v1','production/metrics':'v1','bench-quality-results':'bench-quality','quality-production/metrics':'quality-v2','valve-repair/metrics':'valve-repair','repair-status':'repair'}
    for folder,run_id in folders.items():
        for p in (work/folder).glob('*.json'):
            m=json.loads(p.read_text())
            if 'stem' not in m or 'elapsed_seconds' not in m:continue
            key=(run_id,m['stem'],m['status'])
            if key in seen:continue
            seen.add(key)
            chapter=m.get('chapter',m['stem'].split('_')[0]);r=totals[chapter]
            r['estimated_usd']+=m.get('estimated_usd',0);r['worker_seconds']+=m['elapsed_seconds']
            r['completed_chunks']+=m.get('status')=='complete';r['failed_attempts']+=m.get('status')!='complete'
            records.append(dict(run=run_id,**{k:v for k,v in m.items() if k!='log'}))
    speech={}
    for chapter in ['heart','dna']:
        speech[chapter]={}
        for version,folder in [('discarded_draft','audio-long-draft'),('final_script','audio')]:
            usage=json.loads((work/folder/(chapter+'-usage.json')).read_text())
            speech[chapter][version+'_characters']=usage['characters']
    report=dict(generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),compute=totals,worker_records=records,speech=speech,invoice_verified=False)
    (ROOT/'tests/production-cost-records.json').write_text(json.dumps(report,indent=2))
    names={'cell':'The Fundamental Unit of Life','heart':'Human Heart and Circulation','dna':'DNA: From Gene to Protein'}
    rows=[]
    for k,v in media.items():
        d=v['duration'];rows.append(f'| {names[k]} | {int(d//60)}:{d%60:05.2f} | {v["expected_frames"]:,} | ${totals[k]["estimated_usd"]:.2f} |')
    chars=sum(sum(v.values()) for v in speech.values())
    text='''# Delivery report

Three masters were generated at native **1920×1080, 24 fps, H.264 with 48 kHz AAC narration**. No music is present. Automated checks passed for resolution, codecs, frame rate, exact frame count, duration, audio coverage/sample rate, full-file decoding and absence of sustained black frames. Timestamped contact sheets and the original/recreation comparison accompany the videos.

| Video | Duration | Frames | Measured render estimate |
|---|---:|---:|---:|
'''+ '\n'.join(rows)+f'''

## Cost

Total estimated worker resource cost with completed runtime records is **${sum(v['estimated_usd'] for v in totals.values()):.2f}**. This includes all retained benchmarks, the superseded partial CPU heart pass, recorded unsuccessful attempts and the final production passes. Estimates multiply each worker's measured runtime by the published GPU, CPU and memory rates. They are **not a verified Modal invoice**. Canceled in-flight workers may not have written completion metrics, so their usage is captured by the provider snapshots below rather than this runtime estimate. Build/startup time, brief container idling, final assembly, storage and account credits can also change the billed amount. The detailed ledger is in `visual-learning-pipeline/tests/production-cost-records.json`.

The cell chapter was rendered in `vizuaraai`; the final heart and DNA chapters were rendered in the explicitly authorized `rajatdandekar` workspace. Its billing API confirmed an existing **$250 monthly plan charge** before rendering. That fixed plan charge is separate from this production's metered compute. The original app used 48 samples; the final originals use 128 samples with a stricter adaptive threshold. Superseded CPU outputs are excluded from the final masters. Three heart shots were then rerendered to align blood-cell transit with fully open valves; both the replaced chunks and the correction pass are counted in the cost audit.

ElevenLabs consumed **{chars:,} requested text characters** across both the discarded longer drafts and final scripts. The last subscription check reported zero current overage; existing plan credits were used. No per-request cash invoice was available. Reusing the bundled final FLAC tracks requires no new speech generation.

## Material deviations

- **Reference matching is interpretive.** The cell chapter retains the original audio, overall frame count and broad teaching progression. Its procedural models, camera paths, cuts, interface layout and some actions differ from the source. The reference supplies flattened pictures rather than its editable scene files, and the rebuild uses newly authored procedural scenes and a newly drawn interface. It is not a frame-identical recreation. The comparison shows both versions at the same timestamps.
- **Source science versus source fidelity.** The cell source narration contains scientific errors. It is retained to preserve the requested performance, while visible labels correct protein/lipid synthesis, selective transport, ER–Golgi vesicles, plastids, the nucleoid and cytoplasm/cytosol distinctions. The retained spoken source therefore is not fully scientifically corrected.
- **Model scope.** Assets are original 3D educational schematics. Heart anatomy is not patient imaging; molecular shapes are not atomic-coordinate reconstructions. Some inspection shots use camera movement around repeated assets, and several complex source actions are simplified.
- **Voice timing.** Final speech is generated from newly written Hindi scripts with English terms. Pitch-preserving tempo adjustment is 1.1887× for heart and 1.2525× for DNA to fit approximately eight minutes. Audio signal checks passed; the execution environment did not support a listening review.
- **Local environment.** The actual machine was an M1 Mac with 8 GB RAM. All 131 local composition test frames were shown before cloud spending, at reduced preview resolution. The final frames were rendered in the cloud at native full HD.

## Reproducibility

The repository contains original geometry generators, deterministic animation, final shot manifests, Hindi scripts and aligned subtitles, the final lossless narration, owned source audio, the interface/font assets, durable Modal dispatch/assembly tools and production checksums. Follow `visual-learning-pipeline/README.md`. Do not regenerate the placeholder manifests over the locked final timings.

Pricing reference: [Modal resource pricing](https://modal.com/pricing). Scientific references and full provenance are in the repository's `docs/STYLE_ANALYSIS.md` and `docs/PROVENANCE.md`.
'''
    providers=list((ROOT/'tests').glob('modal-billing-snapshot-*.json'))
    if providers:
        snapshots=[json.loads(p.read_text()) for p in providers]
        total=sum(float(s['total_usd']) for s in snapshots)
        text+=f"\n**Provider-reported cloud usage for this production: ${total:.2f}**, across its isolated apps in both workspaces. Snapshots include the current UTC hour provisionally and were fetched between {min(s['fetched_utc'] for s in snapshots)} and {max(s['fetched_utc'] for s in snapshots)}. They include metered usage from canceled workers. Account plan credits and the fixed subscription fee are not allocated to individual apps. Metering can settle later; this is provider usage as of retrieval, not a final invoice.\n"
    (delivery/'DELIVERY_REPORT.md').write_text(text)
    print('Wrote delivery report from verified masters and worker metrics.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--delivery',type=Path,required=True);a=p.parse_args();run(a.work,a.delivery)
