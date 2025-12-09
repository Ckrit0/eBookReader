// 선택한 책 표시
function accentSelectBook(){
    let bookList = document.getElementsByClassName('bookList')
    for(index in bookList){
        if(bookList[index].innerText == bookInfo['name']){
            bookList[index].style['color']='black'
            bookList[index].style['font-weight']='bold'
        }
    }
    
}

// 상단바 이동
function useNavBar(){
    function movePage(){
        if(volumeInput.value == bookInfo['volume']){
            moveLine(lineInput.value)
        }else{
            window.location.href = "/read/" + bookInfo['name'] + "/" + volumeInput.value + '/' + lineInput.value
        }
    }
    let volumeInput = document.getElementById('headVolume')
    volumeInput.addEventListener('keydown',(e)=>{
        if(e.key == 'Enter'){
            movePage()
        }
    })
    let lineInput = document.getElementById('headLine')
    lineInput.addEventListener('keydown',(e)=>{
        if(e.key == 'Enter'){
            movePage()
        }
    })
    let moveBtn = document.getElementById('headButton')
    moveBtn.addEventListener('click',movePage)
}
