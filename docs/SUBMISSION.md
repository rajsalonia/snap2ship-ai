# MLH Hacktoberfest Delhi submission pack

**Title:** Snap2Ship AI — From Real-World Photos to Working Micro-Apps

**Tagline:** Photograph a problem. Discover feasible apps. Build a verified starting point.

**Problem:** Everyday software needs are hidden inside campus posters, handwritten notes and screenshots. Turning these into a working application usually requires repeatedly drafting requirements, planning UI and manually assembling a project.

**Solution:** Snap2Ship AI uses Gemma 4 to analyze image+text inputs, propose three focused micro-app ideas, show reasons and feasibility estimates, and assemble a downloadable React/Vite project from known-safe templates. Users review the extracted facts and locally run npm build before deployment.

**Stack:** Gemma 4 through the Gemini Developer API; Python FastAPI + Pydantic; React/Vite + CSS; optional DigitalOcean App Platform.

**Innovation/originality:** Inspired by the discover→rank→build→validate workflow showcased by vibeDeploy. Snap2Ship differs in input modality (real-world images and text), target users (students and communities), scope (template-backed micro-apps), explicit source verification, and honest separation of structural checks from actual compile/test/deployment. Not affiliated with the vibeDeploy authors.

**Category A: Best Open-Source AI Project:** The project is available under MIT with reproducible source, template logic, tests and contribution paths. Gemma 4 is an open-weight model family central to the analysis. DigitalOcean is a verified integration only if a DO deployment actually runs.

**Category B: Best Use of Gemma 4:** Gemma 4 is the primary multimodal understanding and idea-planning engine. Users can photograph posters or other real-world information, add text constraints and obtain structured app proposals that the generator turns into a React project. Do not claim image support was tested until a real model call succeeds.

## 2-minute demo plan

- 0:00–0:20: Problem and why normal chat responses aren't sufficient.
- 0:20–0:45: Upload a non-sensitive college event poster with text context; execute real Gemma analysis.
- 0:45–1:10: Show three scoped choices with GO/REVIEW/NO-GO; explain reasoning estimates aren't external market research.
- 1:10–1:35: Select a GO card and build. Show HTML preview and download React/Vite app.
- 1:35–1:50: Show local npm production build verification for downloaded app, if completed.
- 1:50–2:00: Show repo, actual hosting link if deployed, and future enhancements.

## Check before submit

- [ ] Real Gemma image API call succeeded
- [ ] App generated from actual analyzed input
- [ ] Downloaded app passed local `npm run build` (otherwise disclose it was not run)
- [ ] UI and backend tested end-to-end
- [ ] GitHub repo public with MIT license and screenshots
- [ ] README includes setup and safety limitations
- [ ] DO deployment working if claimed
- [ ] Short demo screen recording saved and playable
- [ ] MLH in-person check-in completed
- [ ] Submission accepted before 4 PM IST
