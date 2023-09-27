const copyBtnBox = document.getElementById('copy-btn-box')
const bookIdToCopy = document.getElementById('book-id-box')

copyBtnBox.addEventListener('click', ()=> {
    const bookId = bookIdToCopy.textContent;

    navigator.clipboard.writeText(bookId).then(()=> {
        copyBtnBox.innerHTML = "<p>copied!</p>"
    })
})