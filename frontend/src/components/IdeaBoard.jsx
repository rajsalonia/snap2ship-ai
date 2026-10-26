import React from 'react';
import {ArrowRight, CheckCircle2, Code2, ShieldCheck, Users} from 'lucide-react';

export default function IdeaBoard({analysis, mode, selected, onSelect, onBuild, busy}) {
  return <section className="panel" id="ideas" aria-labelledby="ideas-title">
    <div className="ptitle"><div><span className="kicker">02 / DISCOVER & EVALUATE</span><h2 id="ideas-title">Three possibilities. One next step.</h2></div><span className={'source-badge ' + (mode === 'sample' ? 'sample' : '')}>{mode === 'sample' ? 'Curated sample · no AI call' : 'Gemma 4 response'}</span></div>
    <div className="summary"><b>Problem discovered</b><p>{analysis.problem}</p><small>{analysis.source_summary}</small></div>
    <details className="source-details"><summary>Review extracted source facts <span>{analysis.facts.length} observations</span></summary><p className="smallnote">Source observations can contain extraction errors. Compare them with your original image.</p><ul>{analysis.facts.map((fact, i) => <li key={i}>{fact}</li>)}</ul><p className="smallnote">Suggested next steps: {analysis.actions.join(' · ') || 'None supplied'}</p></details>
    <div className="cards">{analysis.ideas.map((idea, i) => <article key={idea.title} className={'ideacard ' + (selected === i ? 'selected' : '')}>
      <div className="cardtop"><span className={'verdict ' + idea.verdict.toLowerCase().replace('-', '')}>{idea.verdict}</span><strong>{idea.score}<small>/100</small></strong></div>
      <div className="score-track"><span style={{width: `${idea.score}%`}}/></div>
      <h3>{idea.title}</h3><p>{idea.pitch}</p><div className="audience"><Users size={13}/>{idea.audience}</div><span className="complexity">{idea.template === 'event' ? 'Event tracker' : idea.template === 'checklist' ? 'Checklist' : 'Information site'} · {idea.complexity} complexity</span>
      <ul className="feature-list">{idea.features.map((feature, j) => <li key={j}><CheckCircle2 size={12}/>{feature}</li>)}</ul>
      <p className="reason">{idea.reason}</p>
      {idea.score_breakdown && <details className="score-details"><summary>How this score is estimated</summary><dl><div><dt>MVP scope</dt><dd>{idea.score_breakdown.scope}/40</dd></div><div><dt>Template fit</dt><dd>{idea.score_breakdown.template_fit}/35</dd></div><div><dt>Source clarity</dt><dd>{idea.score_breakdown.source_clarity}/25</dd></div></dl></details>}
      <div className="idea-actions"><button className="select-button" onClick={() => onSelect(i)} aria-pressed={selected === i} disabled={busy}>{selected === i ? 'Selected' : 'Select idea'}</button><button className="build-card" onClick={() => onBuild(i)} disabled={busy}><Code2 size={14}/>Build<ArrowRight size={13}/></button></div>
    </article>)}</div>
    <div className="review"><ShieldCheck size={17}/><span><b>Review required:</b> {analysis.confidence_note}</span></div>
    <p className="smallnote">Scores are feasibility estimates for this template builder, not independent market research. GO ≥ 75 · REVIEW ≥ 50 · NO-GO &lt; 50.</p>
  </section>;
}
