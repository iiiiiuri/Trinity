document.getElementById('ano-mais').addEventListener('click', function () {
    let url = new URL(window.location.href)
    let date = url.pathname.split('/').pop()
    let [day, month, year] = date.match(/(\d{2})(\d{2})(\d{4})/).slice(1)
    year = parseInt(year) + 1
    url.pathname = url.pathname.replace(date, `${day}${month}${year}`)
    window.location.href = url.href
  })
  
  document.getElementById('ano-menos').addEventListener('click', function () {
    let url = new URL(window.location.href)
    let date = url.pathname.split('/').pop()
    let [day, month, year] = date.match(/(\d{2})(\d{2})(\d{4})/).slice(1)
    year = parseInt(year) - 1
    url.pathname = url.pathname.replace(date, `${day}${month}${year}`)
    window.location.href = url.href
  })
  
  document.getElementById('mes-mais').addEventListener('click', function () {
    let url = new URL(window.location.href)
    let date = url.pathname.split('/').pop()
    let [day, month, year] = date.match(/(\d{2})(\d{2})(\d{4})/).slice(1)
    month = parseInt(month)
    year = parseInt(year)
    if (month === 12) {
      month = 1
      year += 1
    } else {
      month += 1
    }
    month = ('0' + month).slice(-2)
    url.pathname = url.pathname.replace(date, `${day}${month}${year}`)
    window.location.href = url.href
  })
  
  document.getElementById('mes-menos').addEventListener('click', function () {
    let url = new URL(window.location.href)
    let date = url.pathname.split('/').pop()
    let [day, month, year] = date.match(/(\d{2})(\d{2})(\d{4})/).slice(1)
    month = parseInt(month)
    year = parseInt(year)
    if (month === 1) {
      month = 12
      year -= 1
    } else {
      month -= 1
    }
    month = ('0' + month).slice(-2)
    url.pathname = url.pathname.replace(date, `${day}${month}${year}`)
    window.location.href = url.href
  })