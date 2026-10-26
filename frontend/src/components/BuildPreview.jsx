import React, {useState} from 'react';
import {AlertCircle, CheckCircle2, Download, FileCode2, Monitor, Smartphone, Terminal} from 'lucide-react';

export default function BuildPreview({built, title, onDownload}) {
  const [device, setDevice] = useState('desktop');
  const result = built.validation;
  const passed = result.production_build_passed;
  return <section className="panel" id="preview" aria-labelledby="preview-title">
    <div className="ptitle"><div><span className="kicker">03 / BUILD & VERIFY</span><h2 id="preview-title">{title}</h2></div><span className={'verdict ' + (passed ? 'go' : result.status === 'failed' ? 'nogo' : 'review')}>{passed ? 'BUILD VERIFIED' : result.status === 'failed' ? 'BUILD FAILED' : 'BUILD UNVERIFIED'}</span></div>
    <div className="build-stats"><div><span>Production compiler</span><b>{passed ? 'Passed' : result.status === 'failed' ? 'Failed' : 'Unavailable'}</b></div><div><span>Source files</span><b>{built.files.length}</b></div><div><span>Compile time</span><b>{result.duration_seconds}s</b></div><div><span>Preview</span><b>{built.preview_kind === 'compiled_react' ? 'Actual React build' : 'Static fallback'}</b></div></div>
    <div className="previewheader"><span><span className="mini-dot"/> {built.sample ? 'Fictional sample app' : 'Your generated application'}</span><div className="device-toggle"><button aria-label="Desktop preview" aria-pressed={device === 'desktop'} onClick={() => setDevice('desktop')}><Monitor size={15}/></button><button aria-label="Mobile preview" aria-pressed={device === 'mobile'} onClick={() => setDevice('mobile')}><Smartphone size={15}/></button></div></div>
    <div className={'preview-stage ' + device}><iframe title="Generated app preview" srcDoc={built.preview_html} sandbox="allow-scripts" className="preview"/></div>
    <div className="review">{passed ? <CheckCircle2 size={18}/> : <AlertCircle size={18}/>}<span>{passed ? 'npm run build passed and production HTML, JavaScript and CSS were checked. Try the interactions in the preview. This does not verify factual accuracy or every runtime behavior.' : 'Source files were generated. Production compilation has not passed; inspect the logs before using this app.'}</span></div>
    <div className="artifact-details"><details><summary><Terminal size={15}/>Build logs <span>{result.status}</span></summary><pre>{result.logs.join('\n')}</pre></details><details><summary><FileCode2 size={15}/>Project files <span>{built.files.length} files</span></summary><ul className="file-list">{built.files.map(file => <li key={file.path}><code>{file.path}</code><span>{file.bytes.toLocaleString()} B</span></li>)}</ul></details></div>
    <div className="bottom"><span>React + Vite · lockfile · README · actual build report</span><button onClick={onDownload}><Download size={16}/>Download source ZIP</button></div>
  </section>;
}
