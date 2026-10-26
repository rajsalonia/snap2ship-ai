import React, {useEffect, useRef, useState} from 'react';
import {AlertCircle, ArrowRight, Boxes, BrainCircuit, Camera, CheckCircle2, ChevronRight, Code2, ExternalLink, FileImage, Github, LoaderCircle, Rocket, Upload, X} from 'lucide-react';
import IdeaBoard from './components/IdeaBoard.jsx';
import BuildPreview from './components/BuildPreview.jsx';

const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
const SAMPLE_CONTEXT = 'Campus Create Day is on 14 November 2026 at the Student Activity Centre. Design Jam at 10:00 AM, Web Workshop at 12:00 PM, Project Showcase at 3:00 PM. Bring a laptop and student ID. Help students find sessions and prepare for the day.';

export default function App() {
  const [description, setDescription] = useState('');
  const [image, setImage] = useState('');
  const [imageName, setImageName] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [mode, setMode] = useState('gemma');
  const [selected, setSelected] = useState(0);
  const [built, setBuilt] = useState(null);
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');
  const [lastAction, setLastAction] = useState('analyze');
  const [health, setHealth] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const uploadId = useRef(0);
  const fileInput = useRef(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(API + '/health', {signal: controller.signal})
      .then(response => { if (!response.ok) throw new Error(); return response.json(); })
      .then(setHealth).catch(error => { if (error.name !== 'AbortError') setHealth({ok: false}); });
    return () => controller.abort();
  }, []);
  useEffect(() => {
    if (!busy) { setElapsed(0); return; }
    const interval = setInterval(() => setElapsed(value => value + 1), 1000);
    return () => clearInterval(interval);
  }, [busy]);
  useEffect(() => {
    if (built) document.getElementById('preview')?.scrollIntoView({behavior: 'smooth', block: 'start'});
  }, [built]);

  function invalidate() { setAnalysis(null); setBuilt(null); setError(''); }
  function upload(file) {
    if (!file || busy) return;
    const id = ++uploadId.current;
    if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) { setError('Please choose a PNG, JPEG or WebP image.'); return; }
    if (!file.size || file.size > 5 * 1024 * 1024) { setError('Choose a non-empty image of 5 MB or less.'); return; }
    const reader = new FileReader();
    reader.onerror = () => setError('This file could not be read. Try another image.');
    reader.onload = () => {
      const picture = new Image();
      picture.onload = () => {
        if (id !== uploadId.current) return;
        if (picture.width * picture.height > 16000000) { setError('Resize this image to 16 megapixels or less.'); return; }
        setImage(String(reader.result)); setImageName(file.name); invalidate();
      };
      picture.onerror = () => { if (id === uploadId.current) setError('This file is not a readable image.'); };
      picture.src = String(reader.result);
    };
    reader.readAsDataURL(file);
  }
  async function request(route, body) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 115000);
    try {
      const response = await fetch(API + route, {method: body ? 'POST' : 'GET', headers: body ? {'Content-Type': 'application/json'} : {}, body: body ? JSON.stringify(body) : undefined, signal: controller.signal});
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'The server could not complete this request.');
      return data;
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('The request timed out. Retry or use a smaller image.');
      if (error instanceof TypeError) throw new Error('Could not reach the backend. Check that the API is running and its URL and CORS settings match this site.');
      throw error;
    } finally { clearTimeout(timeout); }
  }
  async function analyze() {
    setBusy('analyze'); setLastAction('analyze'); setError(''); setAnalysis(null); setBuilt(null);
    try { const data = await request('/api/analyze', {description, image_data_url: image || null}); setAnalysis(data); setMode('gemma'); setSelected(0); }
    catch (error) { setError(error.message); }
    finally { setBusy(''); }
  }
  async function loadSample() {
    setBusy('sample'); setLastAction('sample'); setError(''); setBuilt(null); setAnalysis(null);
    try {
      const data = await request('/api/sample');
      const poster = await fetch('/sample-poster.png').then(response => {if (!response.ok) throw new Error('Sample poster could not be loaded.'); return response.blob();});
      const posterUrl = await new Promise((resolve, reject) => {const reader = new FileReader(); reader.onload = () => resolve(String(reader.result)); reader.onerror = reject; reader.readAsDataURL(poster);});
      setAnalysis(data.analysis); setMode('sample'); setSelected(0);
      setDescription(SAMPLE_CONTEXT); setImage(posterUrl); setImageName('Fictional sample poster · no model called');
    } catch (error) { setError(error.message); }
    finally { setBusy(''); }
  }
  async function build(index = selected) {
    if (!analysis) return;
    setSelected(index); setBusy('build'); setLastAction('build'); setError(''); setBuilt(null);
    try { setBuilt(await request('/api/build', {analysis, idea: analysis.ideas[index]})); }
    catch (error) { setError(error.message); }
    finally { setBusy(''); }
  }
  function download() {
    const raw = atob(built.zip_base64);
    const bytes = Uint8Array.from(raw, char => char.charCodeAt(0));
    const href = URL.createObjectURL(new Blob([bytes], {type: 'application/zip'}));
    const anchor = document.createElement('a');
    anchor.href = href; anchor.download = built.filename; document.body.appendChild(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(href), 10000);
  }
  const phase = built ? 3 : busy === 'build' ? 2 : analysis ? 1 : 0;
  const status = !health ? 'Connecting to API' : !health.ok ? 'API unavailable' : health.key_configured ? 'Gemma key configured' : 'Gemma key needed';

  return <div className="shell">
    <aside><a className="brand" href="#studio"><span className="brandicon"><Boxes size={22}/></span><div>snap<span>2</span>ship<small>AI APP FACTORY</small></div></a>
      <div className="sidebarheading">WORKSPACE</div>
      <a className="nav active" href="#studio"><BrainCircuit size={17}/>Builder Studio<ChevronRight size={14}/></a>
      <a className={'nav ' + (!analysis ? 'nav-disabled' : '')} href={analysis ? '#ideas' : '#studio'}><Code2 size={17}/>Idea Discovery<span className="pill">03</span></a>
      <a className={'nav ' + (!built ? 'nav-disabled' : '')} href={built ? '#preview' : '#studio'}><Rocket size={17}/>App Factory</a>
      <div className="sidebar-note"><span>FROM A SMALL SPARK</span><p>Useful software starts with something you notice.</p><div className="tiny-grid"><span>↗</span><span>✦</span><span>⌘</span></div></div>
      <div className="sidebarfoot"><span className={'status-dot ' + (health?.ok ? 'connected' : '')}/>{status}<br/><span>Gemma 4 · Gemini Developer API</span></div>
      <a className="repo-link" href="https://github.com/rajsalonia/snap2ship-ai" target="_blank" rel="noreferrer"><Github size={14}/>View source<ExternalLink size={12}/></a>
    </aside>
    <main className="workspace" id="studio"><div className="topbar"><div><span className="muted">WORKSPACE / </span>Builder Studio</div><div className="tag"><span className="online"/>Open-source · MIT</div></div>
      <div className="wrap"><div className="hero"><div className="sup"><Rocket size={14}/>HACKTOBERFEST 2026 · SNAP2SHIP AI</div><h1>Spot a problem.<br/>Ship <em>the possibility.</em></h1><p>Turn a campus notice, a scribbled idea, or an everyday challenge into a small app you can actually use.</p>
        <div className="hero-meta"><span><FileImage size={14}/>Image + text discovery</span><span><Code2 size={14}/>Three focused app templates</span><span><CheckCircle2 size={14}/>Real compilation checks</span></div>
        <div className="steps" aria-label="Build progress">{['Discover', 'Evaluate', 'Build', 'Verify'].map((name, i) => <span className={i <= phase ? 'current' : ''} key={name} aria-current={i === phase ? 'step' : undefined}><b>{i < phase ? '✓' : String(i + 1).padStart(2, '0')}</b>{name}{i < 3 && <ArrowRight size={13}/>}</span>)}</div>
      </div>
      <section className="panel" aria-labelledby="input-title"><div className="ptitle"><div><span className="kicker">01 / INPUT STUDIO</span><h2 id="input-title">What did you notice?</h2></div><span className="faded"><Camera size={16}/>Multimodal input</span></div>
        <div className="inputgrid"><div className="image-column"><label className={'upload ' + (dragging ? 'dragging' : '')} onDragOver={event => {event.preventDefault(); if (!busy) setDragging(true);}} onDragLeave={() => setDragging(false)} onDrop={event => {event.preventDefault(); setDragging(false); upload(event.dataTransfer.files?.[0]);}}>
          {image ? <><img src={image} alt="Source image preview"/><strong>Choose another image</strong><small>{imageName}</small></> : <><div className="uploadicon"><Upload size={25}/></div><strong>Drop a photo or screenshot</strong><small>or click to browse · PNG, JPEG, WebP</small><span className="upload-limit">UP TO 5 MB · 16 MEGAPIXELS</span></>}
          <input ref={fileInput} type="file" aria-label="Upload source image" accept="image/png,image/jpeg,image/webp" disabled={!!busy} onChange={event => upload(event.target.files?.[0])}/>
        </label>{image && <button className="remove-image" disabled={!!busy} onClick={() => {uploadId.current++; setImage(''); setImageName(''); if (fileInput.current) fileInput.current.value = ''; invalidate();}}><X size={12}/>Remove image</button>}</div>
          <div className="textentry"><label htmlFor="prompt">ADD A LITTLE CONTEXT</label><textarea id="prompt" maxLength={2500} disabled={!!busy} value={description} onChange={event => {setDescription(event.target.value); invalidate();}} placeholder="Students miss deadlines buried in college posters. Help them find useful sessions and plan their next steps…"/><div className="text-foot"><span>Text alone works, too.</span><span>{description.length}/2500</span></div></div></div>
        <div className="sample-row"><span>Need a starting point?</span><button disabled={!!busy} className="text-button" onClick={loadSample}>Try a fictional campus poster<ArrowRight size={13}/></button><span className="sample-disclosure">Curated sample · no AI call</span></div>
        <div className="bottom"><span>Analyzed with <b>Gemma 4</b> · Keep personal data out of uploads</span><button onClick={analyze} disabled={!!busy || (!image && !description.trim())}>{busy === 'analyze' ? <><LoaderCircle className="spin" size={17}/>Analyzing with Gemma…</> : <><BrainCircuit size={17}/>Analyze with Gemma<ArrowRight size={16}/></>}</button></div>
      </section>
      {busy && <div className="activity" role="status" aria-live="polite"><LoaderCircle className="spin" size={18}/><div><b>{busy === 'build' ? 'Assembling your app and running npm run build' : busy === 'analyze' ? 'Gemma is reading your input and planning three ideas' : 'Loading the fictional sample'}</b><span>{busy === 'build' ? 'Trusted React templates · production compiler · output checks' : busy === 'analyze' ? 'Source observations and suggestions will be shown separately.' : 'This sample does not call Gemma.'}</span></div><small>{elapsed}s</small></div>}
      {error && <div className="error" role="alert"><AlertCircle size={19}/><span>{error}</span><button disabled={!!busy} onClick={() => lastAction === 'build' ? build() : lastAction === 'sample' ? loadSample() : analyze()}>Retry</button><button className="dismiss" aria-label="Dismiss error" onClick={() => setError('')}><X size={16}/></button></div>}
      {analysis && <IdeaBoard analysis={analysis} mode={mode} selected={selected} onSelect={index => {setSelected(index); setBuilt(null);}} onBuild={build} busy={!!busy}/>}
      {built && <BuildPreview built={built} title={analysis.ideas[selected].title} onDownload={download}/>}
      {!analysis && !busy && <div className="empty-grid">{[{title: 'Campus event tracker', description: 'Search sessions, save favorites and prepare.', icon: '01'}, {title: 'Task & checklist app', description: 'Add tasks, track progress, keep moving.', icon: '02'}, {title: 'Information website', description: 'Make important details easier to find.', icon: '03'}].map(item => <div key={item.title}><span>{item.icon}</span><h3>{item.title}</h3><p>{item.description}</p></div>)}</div>}
      <footer className="appfoot"><span>SNAP2SHIP AI · FROM REAL-WORLD PROBLEMS TO WORKING APPS</span><span>Gemma access {health?.key_configured ? 'configured, not health-verified' : 'not configured'} · {health?.compiler_available ? 'Compiler ready' : 'Compiler status unavailable'}</span></footer>
    </div></main>
  </div>;
}
