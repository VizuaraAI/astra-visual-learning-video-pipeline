"""Read provider hourly usage and retain only this production's isolated apps."""
import argparse,dataclasses,datetime,json
from pathlib import Path
import modal
NAMES={'vl-execu-20260905','vl-execu-20260905-prod','vl-execu-20260905-quality'}

def run(output,start,include_current=False):
    now=datetime.datetime.now(datetime.timezone.utc)
    end=(now.replace(minute=0,second=0,microsecond=0)+datetime.timedelta(hours=1)) if include_current else now
    rows=modal.Workspace.from_context().billing.report(start=datetime.datetime.fromisoformat(start).replace(tzinfo=datetime.timezone.utc),end=end,resolution='h')
    ours=[dataclasses.asdict(x) for x in rows if x.description in NAMES]
    report=dict(fetched_utc=now.isoformat(),complete_intervals_only=not include_current,total_usd=str(sum((x['cost'] for x in ours),start=0)),rows=ours)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,default=str,indent=2))
    print('Provider-reported usage:',report['total_usd'],'(current hour provisional)' if include_current else '(completed UTC hours)')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--start',default='2026-09-05T08:00:00');p.add_argument('--include-current',action='store_true');a=p.parse_args();run(a.output,a.start,a.include_current)
