(function () {
  var PROJECTS = [
    {
      id: 'bnw',
      url: 'bnw_film_photo.html',
      name: 'Series 02',
      type: 'Photography',
      imgA: 'Bnw_film_photo/000021.webp',
      imgB: 'Bnw_film_photo/000009.webp'
    },
    {
      id: 'tokyo',
      url: '/tokyo',
      name: 'Tokyo Night Drive',
      type: 'Documentary',
      imgA: 'images/tokyo.png',
      imgB: 'TokyoRender/Logo2.png'
    },
    {
      id: 'prada',
      url: '/prada',
      name: 'Prada',
      type: 'Visual Identity',
      imgA: 'images/prada.jpg',
      imgB: 'prada/Mockup_city.jpg'
    },
    {
      id: 'nike',
      url: '/nike',
      name: 'Nike \u2014 Turn On',
      type: 'Campaign',
      imgA: 'images/nike.jpg',
      imgB: 'NikeRender/billboard.png'
    },
    {
      id: 'oakley',
      url: '/oakley',
      name: 'Oakley',
      type: 'Brand System',
      imgA: 'images/oakley.png',
      imgB: 'Oakley/Frame.Still001.jpg'
    },
    {
      id: 'morocco',
      url: '/morocco',
      name: 'Morocco',
      type: 'Visual Study',
      imgA: 'images/morocco.jpg',
      imgB: '03_RENDER/frame2Color.jpg'
    },
    {
      id: 'bold-agency',
      url: '/bold-agency',
      name: 'Bold Agency',
      type: 'Digital',
      imgA: 'images/bold-agency.jpg',
      imgB: 'BoldRender/mockupsite.jpg'
    },
    {
      id: 'photography',
      url: '/photography',
      name: 'Series 01',
      type: 'Photography',
      imgA: 'Film_photo/A022232-R1-07-5A.webp',
      imgB: 'Film_photo/A022232-R1-08-7A.webp'
    },
    {
      id: 'vecchia',
      url: '/vecchia',
      name: 'La Vecchia Signora',
      type: 'Branding',
      imgA: 'images/vecchia.png',
      imgB: 'restaurantRender/updated.jpg'
    },
    {
      id: 'tam',
      url: '/tam',
      name: 'TAM Gratuit Pour Tous',
      type: 'Editorial',
      imgA: 'images/tam.jpg',
      imgB: 'TamRender/Mockup1.png'
    }
  ];

  var currentId = window.CURRENT_PROJECT;
  var grid = document.getElementById('related-grid');
  if (!grid) return;

  // Filter out current page
  var pool = PROJECTS.filter(function (p) { return p.id !== currentId; });

  // Fisher-Yates shuffle
  for (var i = pool.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp;
  }

  // Render 3 cards
  pool.slice(0, 3).forEach(function (p) {
    var item = document.createElement('div');
    item.className = 'related-item';

    var a = document.createElement('a');
    a.href = p.url;
    a.className = 'project related-card';

    var imgWrap = document.createElement('div');
    imgWrap.className = 'project-img';

    var imgA = document.createElement('img');
    imgA.className = 'img-a';
    imgA.src = p.imgA;
    imgA.alt = p.name;
    imgA.loading = 'lazy';

    var imgB = document.createElement('img');
    imgB.className = 'img-b';
    imgB.src = p.imgB;
    imgB.alt = p.name + ' alternate';
    imgB.loading = 'lazy';
    imgB.decoding = 'async';

    imgWrap.appendChild(imgA);
    imgWrap.appendChild(imgB);

    var nameSpan = document.createElement('span');
    nameSpan.className = 'project-name';
    nameSpan.textContent = p.name;

    var typeSpan = document.createElement('span');
    typeSpan.className = 'project-type';
    typeSpan.textContent = p.type;

    a.appendChild(imgWrap);
    a.appendChild(nameSpan);
    a.appendChild(typeSpan);
    item.appendChild(a);
    grid.appendChild(item);
  });

  // Page-transition click handler
  grid.querySelectorAll('.related-card').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var href = this.getAttribute('href');
      var layout = document.querySelector('.body-layout');
      var spacer = document.querySelector('.spacer');
      sessionStorage.setItem('vt-from', 'project');
      [layout, spacer].filter(Boolean).forEach(function (el) {
        el.style.transition = 'opacity 0.35s ease';
        el.style.opacity = '0';
      });
      setTimeout(function () { window.location.href = href; }, 360);
    });
  });
})();
