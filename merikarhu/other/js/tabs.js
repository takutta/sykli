const triggerTabList = document.querySelectorAll('#nav-tab')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault()
    alert($($(this).attr('href')).index());
    tabTrigger.show()
  })
})