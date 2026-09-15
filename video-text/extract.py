import argparse,json,sys,tempfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--output',default='outputs');p.add_argument('--model',default='small');p.add_argument('--language',default='zh');p.add_argument('--browser');a=p.parse_args(); task={}
 if a.source.endswith('.pku-video.json'): task=json.loads(Path(a.source).read_text()); url=task['url']; title=task.get('title','课程')
 else: url=a.source; title='教学视频'
 import yt_dlp
 out=Path(a.output)/title;out.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as d:
  o={'format':'bestaudio/best','outtmpl':d+'/audio.%(ext)s','noplaylist':True}
  if a.browser:o['cookiesfrombrowser']=(a.browser,)
  with yt_dlp.YoutubeDL(o) as y: f=Path(y.prepare_filename(y.extract_info(url,download=True)))
  from faster_whisper import WhisperModel
  m=WhisperModel(a.model,device='cpu',compute_type='int8'); segs,_=m.transcribe(str(f),language=None if a.language=='auto' else a.language,vad_filter=True)
  lines=[title,'']
  for s in segs: lines.append(f'[{int(s.start//3600):02d}:{int(s.start%3600//60):02d}:{int(s.start%60):02d}] {s.text.strip()}')
 (out/'全文.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(out/'全文.txt')
if __name__=='__main__':
 try: main()
 except Exception as e: print('处理失败：',e,file=sys.stderr);sys.exit(1)
