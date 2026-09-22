const IMAGE_EXT = /\.(png|jpe?g|gif|webp|bmp|svg)$/i;
const VIDEO_EXT = /\.(mp4|webm|mov|ogg)$/i;
const MEDIA_EXT = /\.(png|jpe?g|gif|webp|bmp|svg|mp4|webm|mov|ogg)$/i;

const params = new URLSearchParams(window.location.search);
const projectId = params.get("id");
const project = PROJECTS[projectId];

const titleEl = document.getElementById("demo-title");
const summaryEl = document.getElementById("demo-summary");
const statusEl = document.getElementById("demo-status");
const actionsEl = document.getElementById("demo-actions");
const videosEl = document.getElementById("demo-videos");
const imagesEl = document.getElementById("demo-images");

if (!project) {
  titleEl.textContent = "Project not found";
  summaryEl.textContent = "That demo link does not match a project on this site.";
  statusEl.textContent = "";
} else {
  document.title = `${project.title} — Demo`;
  titleEl.textContent = project.title;
  summaryEl.textContent = project.summary;
  const githubUrl = `https://github.com/${GITHUB_USER}/${project.github}`;
  actionsEl.innerHTML = `
    <a class="btn" href="${githubUrl}" target="_blank" rel="noreferrer">Open GitHub repo</a>
    <a class="btn ghost" href="index.html">Back to work</a>
  `;
  loadLocalDemos(project).catch((error) => {
    statusEl.textContent = `Could not load demos (${error.message}).`;
  });
}

async function loadLocalDemos(project) {
  const demoFolder = `demos/${projectId}`;
  console.log(`Loading demos from local folder: ${demoFolder}`);
  
  try {
    // Try to load from local folder
    const response = await fetch(`${demoFolder}/manifest.json`);
    if (!response.ok) {
      throw new Error(`No manifest found in ${demoFolder}`);
    }
    
    const manifest = await response.json();
    console.log(`Loaded manifest with ${manifest.images?.length || 0} images and ${manifest.videos?.length || 0} videos`);
    
    if (!manifest.images && !manifest.videos) {
      statusEl.textContent = "No images or videos configured in manifest.json.";
      return;
    }
    
    const images = manifest.images || [];
    const videos = manifest.videos || [];
    
    if (images.length === 0 && videos.length === 0) {
      statusEl.textContent = "No images or videos configured in manifest.json. Add entries to display your demo media.";
      return;
    }
    
    statusEl.textContent = `${images.length} image${images.length === 1 ? "" : "s"} · ${videos.length} video${videos.length === 1 ? "" : "s"} from local storage`;
    
    // Load videos
    for (const item of videos) {
      try {
        const wrap = document.createElement("figure");
        wrap.className = "demo-video";
        const video = document.createElement("video");
        video.controls = true;
        video.playsInline = true;
        video.preload = "metadata";
        video.src = `${demoFolder}/${item.url}`;
        
        // Add error handling for video
        video.onerror = () => {
          console.warn(`Video failed to load: ${item.url}`);
          wrap.innerHTML = `<p class="demo-error">Video not found: ${item.url}</p>`;
        };
        
        wrap.appendChild(video);
        const figcaption = document.createElement("figcaption");
        figcaption.textContent = item.name;
        wrap.appendChild(figcaption);
        videosEl.appendChild(wrap);
      } catch (error) {
        console.error(`Error loading video ${item.url}:`, error);
      }
    }
    
    // Load images
    for (const item of images) {
      try {
        const imageResponse = await fetch(`${demoFolder}/${item.url}`);
        if (imageResponse.ok) {
          const link = document.createElement("a");
          link.href = `${demoFolder}/${item.url}`;
          link.target = "_blank";
          link.rel = "noreferrer";
          link.className = "demo-shot";
          link.innerHTML = `<img src="${demoFolder}/${item.url}" alt="${item.name}" loading="lazy" /><span>${item.name}</span>`;
          imagesEl.appendChild(link);
        } else {
          console.warn(`Image file not found: ${item.url}`);
          const errorMsg = document.createElement("p");
          errorMsg.className = "demo-error";
          errorMsg.textContent = `Image not found: ${item.url}`;
          imagesEl.appendChild(errorMsg);
        }
      } catch (error) {
        console.error(`Error loading image ${item.url}:`, error);
      }
    }
    
    // Show help message if no files were successfully loaded
    if (videosEl.children.length === 0 && imagesEl.children.length === 0) {
      statusEl.textContent = "No demo files found. Add images/videos to the demos folder and update manifest.json.";
    }
    
  } catch (error) {
    console.error("Error loading local demos:", error);
    statusEl.innerHTML = `Demo folder not set up. Create folder 'demos/${projectId}' with manifest.json and add your images/videos.`;
  }
}
