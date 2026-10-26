import React, {useEffect, useState} from 'react';
import content from './content.json';
import './style.css';

// Storage is optional: the sandboxed embedded preview has an opaque origin.
function useSavedState(name, initial) {
  const key = `snap2ship:${content.id}:${name}`;
  const [value, setValue] = useState(() => {
    try { return JSON.parse(localStorage.getItem(key)) ?? initial; }
    catch { return initial; }
  });
  useEffect(() => { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} }, [key, value]);
  return [value, setValue];
}

function Checklist() {
  const [tasks, setTasks] = useSavedState('tasks', content.tasks.map((text, i) => ({id: `seed-${i}`, text, done: false})));
  const [draft, setDraft] = useState('');
  const [filter, setFilter] = useState('all');
  const completed = tasks.filter(task => task.done).length;
  function add(event) {
    event?.preventDefault();
    if (!draft.trim()) return;
    setTasks(items => [...items, {id: `${Date.now()}-${Math.random()}`, text: draft.trim(), done: false}]);
    setDraft('');
  }
  return <section id={content.type === 'event' ? 'tasks' : 'workspace'} className="card">
    <div className="section-head"><div><p className="eyebrow">YOUR NEXT STEPS</p><h2>Make progress, one task at a time.</h2></div><b className="count">{completed}/{tasks.length}</b></div>
    <progress aria-label="Checklist completion" value={completed} max={tasks.length || 1}/>
    <div className="add-task"><input aria-label="New task" placeholder="Add your next step…" maxLength={300} value={draft} onChange={event => setDraft(event.target.value)} onKeyDown={event => {if (event.key === 'Enter') add(event);}}/><button onClick={add} disabled={!draft.trim()}>Add task</button></div>
    <div className="tabs" aria-label="Task filters">{['all','active','done'].map(value => <button key={value} aria-pressed={filter === value} onClick={() => setFilter(value)}>{value}</button>)}</div>
    <div className="tasks">{tasks.filter(task => filter === 'all' || (filter === 'done' ? task.done : !task.done)).map(task => <div className={'task ' + (task.done ? 'completed' : '')} key={task.id}>
      <label><input type="checkbox" checked={task.done} onChange={() => setTasks(items => items.map(item => item.id === task.id ? {...item, done: !item.done} : item))}/><span>{task.text}</span></label>
      <button className="delete" aria-label={`Delete ${task.text}`} onClick={() => setTasks(items => items.filter(item => item.id !== task.id))}>×</button>
    </div>)}</div>
    {!tasks.length && <p className="empty">Your checklist is clear. Add a task to get started.</p>}
    <p className="hint">Changes stay in this browser when storage is available. Embedded preview changes last for this preview session.</p>
  </section>;
}

function EventTracker() {
  const [query, setQuery] = useState('');
  const [saved, setSaved] = useSavedState('saved-events', []);
  const [savedOnly, setSavedOnly] = useState(false);
  const events = content.events.filter((event, index) => (!savedOnly || saved.includes(index)) && `${event.title} ${event.location} ${event.when}`.toLowerCase().includes(query.toLowerCase()));
  return <section id="workspace" className="card"><div className="section-head"><div><p className="eyebrow">CAMPUS CALENDAR</p><h2>Find your next moment.</h2></div><b className="count">{saved.length} saved</b></div>
    <div className="toolbar"><input aria-label="Search events" placeholder="Search events or locations…" value={query} onChange={event => setQuery(event.target.value)}/><button aria-pressed={savedOnly} className="secondary" onClick={() => setSavedOnly(value => !value)}>{savedOnly ? 'Show all events' : 'Saved events'}</button></div>
    <div className="event-grid">{events.map(event => {const index = content.events.indexOf(event); const isSaved = saved.includes(index); return <article className="event" key={index}><p className="eyebrow">{event.when || 'Date not provided'}</p><h3>{event.title}</h3><p className="location">{event.location || 'Location not provided'}</p><p>{event.detail}</p><button aria-pressed={isSaved} className={isSaved ? 'secondary' : ''} onClick={() => setSaved(items => isSaved ? items.filter(value => value !== index) : [...items, index])}>{isSaved ? 'Saved · remove' : 'Save event'}</button></article>;})}</div>
    {!events.length && <p className="empty">No matching events. Try another search or show all events.</p>}
  </section>;
}

function Information() {
  const [query, setQuery] = useState('');
  const sections = content.sections.filter(section => `${section.heading} ${section.body}`.toLowerCase().includes(query.toLowerCase()));
  return <section id="workspace" className="card"><p className="eyebrow">THE ESSENTIALS</p><h2>Everything you need to know.</h2>
    <input aria-label="Search information" className="info-search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Find information…"/>
    {sections.map((section, index) => <details key={section.heading} open={index === 0}><summary>{section.heading}</summary><p>{section.body}</p></details>)}
    {!sections.length && <p className="empty">No matching information. Try a different search.</p>}
    <a className="text-link" href="#top">Back to top ↑</a>
  </section>;
}

export default function App() {
  return <main className="container" id="top">
    <nav><a className="wordmark" href="#top"><span className="mark">S</span>{content.title}</a><a href="#workspace">{content.type === 'event' ? 'Explore events' : content.type === 'checklist' ? 'My checklist' : 'Explore guide'} ↗</a></nav>
    <header><div className="hero-copy"><p className="eyebrow">BUILT FOR {content.audience}</p><h1>{content.title}</h1><p>{content.tagline}</p><a className="cta" href="#workspace">Get started <span>↗</span></a></div><div className="hero-art" aria-hidden="true"><div className="orbit"></div><span>{content.type === 'event' ? '◷' : content.type === 'checklist' ? '✓' : 'i'}</span><p>Small app.<br/>Real possibility.</p></div></header>
    <div className="pills">{content.features.map(feature => <span key={feature}>{feature}</span>)}</div>
    {content.type === 'event' ? <><EventTracker/><Checklist/></> : content.type === 'checklist' ? <Checklist/> : <Information/>}
    <section className="source card"><p className="eyebrow">SOURCE DETAILS · REVIEW REQUIRED</p><div className="facts">{content.facts.length ? content.facts.map((fact, i) => <p key={i}>{fact}</p>) : <p>No source facts provided.</p>}</div></section>
    <footer><span>Made with Snap2Ship AI · MIT</span><p>{content.verification}</p>{content.sample && <b>Fictional sample · no live model analysis</b>}</footer>
  </main>;
}
