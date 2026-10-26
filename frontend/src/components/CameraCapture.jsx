import React, {useEffect, useRef, useState} from 'react';
import {Camera, CameraOff, Check, RefreshCcw, X} from 'lucide-react';

/** Browser camera is only accessed after the user opens this dialog. No frames are uploaded until "Use photo". */
export default function CameraCapture({onClose, onCapture}) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [error, setError] = useState('');
  const [ready, setReady] = useState(false);
  const [snapshot, setSnapshot] = useState('');
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const closeOnEscape = (event) => { if (event.key === 'Escape') onClose(); };
    document.addEventListener('keydown', closeOnEscape);
    async function start() {
      if (!navigator.mediaDevices?.getUserMedia) {
        setError('Camera capture requires HTTPS or localhost. Use Upload Image instead.');
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({audio: false, video: {facingMode: {ideal: 'environment'}, width: {ideal: 1920}, height: {ideal: 1080}}});
        if (cancelled) { stream.getTracks().forEach(track => track.stop()); return; }
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play().catch(() => {});
          setReady(true);
        }
      } catch (reason) {
        if (!cancelled) setError(reason?.name === 'NotAllowedError' ? 'Camera permission was denied. Allow camera access in your browser or upload a photo.' : 'Camera is unavailable. You can upload an existing image instead.');
      }
    }
    start();
    return () => {
      cancelled = true;
      document.removeEventListener('keydown', closeOnEscape);
      streamRef.current?.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    };
  }, [onClose]);

  function takePhoto() {
    const video = videoRef.current;
    if (!video || !video.videoWidth) return;
    const canvas = document.createElement('canvas');
    const maxSide = 1920;
    const scale = Math.min(1, maxSide / Math.max(video.videoWidth, video.videoHeight));
    canvas.width = Math.max(1, Math.round(video.videoWidth * scale));
    canvas.height = Math.max(1, Math.round(video.videoHeight * scale));
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    setSnapshot(canvas.toDataURL('image/jpeg', 0.86));
    streamRef.current?.getTracks().forEach(track => track.stop());
    streamRef.current = null;
  }
  async function usePhoto() {
    if (!snapshot || capturing) return;
    setCapturing(true);
    try {
      const response = await fetch(snapshot);
      const blob = await response.blob();
      if (!blob.size) throw new Error('The photo is empty.');
      onCapture(new File([blob], 'camera-photo-' + Date.now() + '.jpg', {type: 'image/jpeg'}));
    } catch {
      setError('Could not save this photo. Please try again.');
      setCapturing(false);
    }
  }
  function retake() {
    setSnapshot('');
    setReady(false);
    setError('Close and reopen the camera to take another photo.');
  }

  return <div className="camera-backdrop" role="presentation" onMouseDown={event => {if (event.target === event.currentTarget) onClose();}}>
    <section className="camera-dialog glass" role="dialog" aria-modal="true" aria-labelledby="camera-title">
      <header className="camera-heading"><div><span className="kicker">IMAGE STUDIO</span><h2 id="camera-title">Capture the starting point</h2><p>Your camera stays on this device. Only the photo you choose is sent for Gemma analysis.</p></div><button type="button" className="camera-close" aria-label="Close camera" onClick={onClose}><X size={18}/></button></header>
      <div className="camera-viewport">
        {snapshot ? <img className="camera-photo" alt="Captured photo preview" src={snapshot}/> : <video ref={videoRef} autoPlay playsInline muted aria-label="Live camera preview"/>}
        {!ready && !snapshot && !error && <div className="camera-wait"><Camera size={23}/><span>Requesting camera access…</span></div>}
        {error && <div className="camera-wait"><CameraOff size={24}/><span role="alert">{error}</span></div>}
        {ready && !snapshot && <span className="camera-guides" aria-hidden="true"/>}
      </div>
      <footer className="camera-buttons">
        <button type="button" className="glass-button" onClick={onClose}>{error ? 'Use upload instead' : 'Cancel'}</button>
        {snapshot ? <><button type="button" className="glass-button" onClick={retake}><RefreshCcw size={15}/>Retake</button><button type="button" className="primary-action" disabled={capturing} onClick={usePhoto}><Check size={16}/>Use photo</button></>
          : <button type="button" className="primary-action" disabled={!ready || !!error} onClick={takePhoto}><Camera size={16}/>Take photo</button>}
      </footer>
    </section>
  </div>;
}
