var videoData = new XMLHttpRequest()
videoData.open("GET", "http://192.168.56.1:5000/api/videos")
videoData.onload = function () {
  var myData = JSON.parse(videoData.responseText)
  console.log(myData)
  renderHTML(myData)
}
videoData.send()

function videoCardTemplate(video) {
  return `
    <div id="movie-card" class="card col-sm" style="width: 18rem;">
      <img src="../static/img/${video.thumbnail_photo}" class="card-img-top" alt="...">
      <ul class="list-group list-group-flush">
          <li class="list-group-item">${video.date}</li>
          <li class="list-group-item">${video.time}</li>
      </ul>
      <div class="card-body">
          <a href="#" class="card-link">Ansehen</a>
      </div>
    </div>
  `
}

function renderHTML(myData) {
  document.getElementById("app").innerHTML = `
  ${myData.map(videoCardTemplate).join("")}
  `
}
