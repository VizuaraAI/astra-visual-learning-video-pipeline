"""Read provider hourly usage and retain only this production's two isolated apps."""
import argparse,dataclasses,datetime,json
from pathlib import Path
import modal
NAMES={'vl-execu-20260905','vl-execu-20260905-prod'}

def run(output,start):
    now=datetime.datetime.now(datetime.timezone.utc)
    rows=modal.Workspace.from_context().billing.report(start=datetime.datetime.fromisoformat(start).replace(tzinfo=datetime.timezone.utc),resolution='h')
    ours=[dataclasses.asdict(x) for x in rows if x.description in NAMES]
    report=dict(fetched_utc=now.isoformat(),complete_intervals_only=True,total_usd=str(sum((x['cost'] for x in ours),start=0)),rows=ours)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,default=str,indent=2))
    print('Provider-reported usage for completed UTC hours:',report['total_usd'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--start',default='2026-09-05T08:00:00');a=p.parse_args();run(a.output,a.start)
