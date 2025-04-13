let gridSize = 0;

function startGame() {
  gridSize = document.getElementById('sizeInput').value;
  fetch('/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ size: gridSize })
  })
  .then(res => res.json())
  .then(updateGrid);
}

function move(dir) {
  fetch('/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ direction: dir })
  })
  .then(res => res.json())
  .then(updateGrid);
}

function runAI() {
  fetch('/ai')
    .then(res => res.json())
    .then(data => {
      let steps = data.steps;
      let i = 0;

      function step() {
        if (i < steps.length) {
          renderGrid({ grid: steps[i].grid });
          document.getElementById('status').innerText =
            steps[i].status || `AI Exploring: (${steps[i].pos[0]}, ${steps[i].pos[1]})`;
          i++;
          setTimeout(step, 500); // smoother & faster animation
        } else {
          document.getElementById('status').innerText = 'AI Finished';
        }
      }

      step();
    });
}

function updateGrid(data) {
  renderGrid({ grid: data.grid });
  document.getElementById('status').innerText = data.status || 'Playing';
}

function renderGrid(data) {
  const grid = data.grid;
  const container = document.getElementById('grid');
  container.innerHTML = '';
  container.style.gridTemplateColumns = `repeat(${gridSize}, 48px)`; // match CSS size

  grid.forEach(row => {
    row.forEach(cell => {
      const div = document.createElement('div');
      div.classList.add('grid-cell'); // updated to match style.css
      div.classList.add(`cell-${cell}`); // assign appropriate class for each image
      container.appendChild(div);
    });
  });
}
