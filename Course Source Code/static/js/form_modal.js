const formModal = document.getElementById('form-modal')
console.log(formModal)

const openModalBtn = document.getElementById('open-modal-btn')
const cancelBtn = document.getElementById('cancel-btn')
const backdrop = document.getElementById('backdrop')

openModalBtn.addEventListener('click', ()=> {
    formModal.classList.remove('hidden')
})

formModal.addEventListener('click', ((e)=> {
    console.log(e.target)
    if (e.target !== backdrop) return;
    formModal.classList.add('hidden')
}))

cancelBtn.addEventListener('click', ()=> {
    formModal.classList.add('hidden')
})