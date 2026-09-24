'use client';
import {useEffect,useState} from 'react';

const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
const card={background:'#111217',border:'1px solid #292c36',borderRadius:18,padding:20};
const btn={background:'#f4f5f7',color:'#08090b',border:0,borderRadius:10,padding:'10px 15px',fontWeight:800,cursor:'pointer'};

export default function Home(){
 const [jobs,setJobs]=useState([]),[apps,setApps]=useState([]),[cvs,setCvs]=useState([]),[tab,setTab]=useState('overview'),[busy,setBusy]=useState(false);
 async function load(){
  const [j,a,c]=await Promise.all([
   fetch(API+'/api/jobs/').then(r=>r.json()),
   fetch(API+'/api/applications/').then(r=>r.json()),
   fetch(API+'/api/cvs/').then(r=>r.json())
  ]);
  setJobs(j);setApps(a);setCvs(c);
 }
 useEffect(()=>{load()},[]);
 async function seed(){setBusy(true);await fetch(API+'/api/jobs/seed',{method:'POST'});await load();setBusy(false)}
 async function prepare(id){await fetch(API+'/api/applications/prepare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({job_id:id})});await load()}
 async function approve(id){await fetch(API+`/api/applications/${id}/approve`,{method:'POST'});await load()}
 async function upload(e){if(!e.target.files[0])return;const f=new FormData();f.append('file',e.target.files[0]);await fetch(API+'/api/cvs/upload',{method:'POST',body:f});await load()}

 const nav=[['overview','◈ Overview'],['jobs','⌕ Job Discovery'],['applications','✉ Applications'],['cv','▣ CV Studio'],['contacts','♙ Contacts'],['settings','⚙ Settings']];

 return <div style={{display:'grid',gridTemplateColumns:'235px 1fr',minHeight:'100vh'}}>
  <aside style={{borderRight:'1px solid #22242c',padding:24}}>
   <h2 style={{margin:'0 0 6px'}}>JOBOS <span style={{fontSize:9,color:'#8d92a2'}}>BETA</span></h2>
   <p style={{fontSize:12,color:'#858998',marginBottom:25}}>AI Career Operating System</p>
   {nav.map(([id,label])=><button key={id} onClick={()=>setTab(id)} style={{display:'block',width:'100%',textAlign:'left',background:tab===id?'#1c1f28':'transparent',color:'#fff',border:0,borderRadius:10,padding:'12px 10px',margin:'4px 0',cursor:'pointer'}}>{label}</button>)}
  </aside>
  <main style={{padding:'34px 38px',maxWidth:1250,width:'100%',boxSizing:'border-box'}}>
   {tab==='overview'&&<><div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><div><h1 style={{fontSize:36,margin:'0 0 5px'}}>Your career command center.</h1><p style={{color:'#9498a7'}}>Discover. Tailor. Connect. Apply.</p></div><button style={btn} onClick={seed}>{busy?'Scanning…':'Run Job Scout'}</button></div>
    <Stats jobs={jobs} apps={apps} cvs={cvs}/>
    <h2>Priority opportunities</h2><JobList jobs={jobs.slice(0,5)} prepare={prepare}/>
   </>}
   {tab==='jobs'&&<><Header title="Job Discovery" action={<button style={btn} onClick={seed}>Scan opportunities</button>}/><JobList jobs={jobs} prepare={prepare}/></>}
   {tab==='applications'&&<><Header title="Applications"/>{apps.length?apps.map(a=><Application key={a.id} a={a} approve={approve}/>):<Empty text="No applications prepared yet."/ >}</>}
   {tab==='cv'&&<><Header title="CV Studio"/><div style={card}><h3>Master CV</h3><p style={{color:'#9599a8'}}>Upload the source CV. Tailoring uses it as the evidence base.</p><input type="file" accept=".pdf,.docx,.txt" onChange={upload}/>{cvs.map(c=><div key={c.id} style={{marginTop:12}}>✓ {c.filename} {c.is_master?'· MASTER':''}</div>)}</div></>}
   {tab==='contacts'&&<><Header title="Recruiter & Contact Hub"/><div style={card}><h3>Contact strategy</h3><p style={{color:'#999dab'}}>The next connector layer can populate permitted public recruiter/hiring-manager data per opportunity. Keep outbound actions approval-first.</p></div></>}
   {tab==='settings'&&<><Header title="Agent Settings"/><div style={card}><h3>Targeting</h3><p>Change the agent without editing Python by using <code>backend/.env</code>.</p><pre style={{lineHeight:1.7,color:'#c7cad4'}}>TARGET_ROLES=AI Creative Technologist,...{"\n"}TARGET_LOCATIONS=Lisbon,Portugal,Nice,France,...{"\n"}MIN_MATCH_SCORE=75{"\n"}MIN_SALARY=65000{"\n"}RELOCATION=true{"\n"}SPONSORSHIP=true</pre></div></>}
  </main>
 </div>
}

function Stats({jobs,apps,cvs}){const data=[['Jobs found',jobs.length],['80%+ matches',jobs.filter(j=>j.match_score>=80).length],['Ready for review',apps.filter(a=>a.status==='ready_for_approval').length],['Master CV',cvs.length?'Ready':'Missing']];return <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:14,margin:'28px 0'}}>{data.map(([a,b])=><div style={card} key={a}><small style={{color:'#858a99'}}>{a}</small><div style={{fontSize:27,fontWeight:850,marginTop:7}}>{b}</div></div>)}</div>}
function Header({title,action}){return <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:25}}><h1>{title}</h1>{action}</div>}
function Empty({text}){return <div style={card}>{text}</div>}
function JobList({jobs,prepare}){return jobs.length?<div>{jobs.map(j=><div style={{...card,margin:'12px 0',display:'flex',justifyContent:'space-between',gap:20}} key={j.id}><div><div style={{fontSize:19,fontWeight:800}}>{j.title}</div><div style={{color:'#999dac',margin:'6px 0'}}>{j.company} · {j.location}</div><div style={{color:'#c9cbd4',fontSize:13}}>{j.description}</div><small style={{display:'block',marginTop:10,color:'#777c8a'}}>{j.sponsorship?'Sponsorship · ':''}{j.relocation?'Relocation · ':''}{j.source}</small></div><div style={{textAlign:'right',minWidth:145}}><div style={{fontSize:26,fontWeight:900}}>{j.match_score}%</div><small style={{color:'#858998'}}>MATCH</small><br/><button style={{...btn,marginTop:12}} onClick={()=>prepare(j.id)}>Prepare</button></div></div>)}</div>:<Empty text="No opportunities yet. Run Job Scout."/>}
function Application({a,approve}){return <div style={{...card,margin:'12px 0'}}><b>Application #{a.id}</b><span style={{marginLeft:10,color:'#a2a6b4'}}>{a.status}</span><details style={{marginTop:14}}><summary>View generated package</summary><pre style={{whiteSpace:'pre-wrap',color:'#cdd0d9',lineHeight:1.5}}>{a.email_body}</pre><hr style={{borderColor:'#292c35'}}/><pre style={{whiteSpace:'pre-wrap',color:'#cdd0d9',lineHeight:1.5}}>{a.tailored_cv}</pre></details>{a.status==='ready_for_approval'&&<button style={{...btn,marginTop:14}} onClick={()=>approve(a.id)}>Approve package</button>}</div>}
