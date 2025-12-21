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

// 페이지 이동
function noExistPage(preOrNext){
    if(preOrNext == 0){
        alert("첫 페이지입니다.")
    }else{
        alert("마지막 페이지입니다.")
    }
}

// line input update
function findLine(){
    let cl = document.getElementById('contentLine')
    let clRect = cl.getBoundingClientRect()
    let coordX = ( clRect.left + clRect.right ) / 2
    let coordY = clRect.top
    let nowPages = []
    for(var i=10; i<30; i+=10){
        nowPages.push(document.elementFromPoint(coordX, coordY + i).id.replace('c_',''))

    }
    for(var i=0; i<3; i++){
        if(!isNaN(nowPages[i])){
            document.getElementById('headLine').value = nowPages[i]
            break
        }
    }
}

// 원하는 라인으로 이동
function moveLine(toLineNumber){
    function getLines(){
        let tempLines = cl.childNodes
        let lines = []
        for(var i=0; i<tempLines.length; i++){
            if(tempLines[i].id === undefined){
                
            }else{
                lines.push([i,tempLines[i].getBoundingClientRect().top])
            }
        }
        return lines
    }
    
    function getScrollCoord(lines, toLineNumber){
        if(toLineNumber > lines.length){
            toLineNumber = lines[lines.length-1][1]
        }else if(toLineNumber < 1){
            toLineNumber = 1
        }
        var moveScrollCoord = lines[toLineNumber-1][1] - lines[0][1]
        return moveScrollCoord
    }
    let cl = document.getElementById('contentLine')
    let lines = getLines()
    let moveScrollCoord = getScrollCoord(lines,toLineNumber)
    cl.scrollTo({top:moveScrollCoord,behavior:"smooth"})
}

// 스크롤 이벤트리스너 등록
function setScrollEvent(){
    let cl = document.getElementById('contentLine')
    cl.addEventListener('scroll',findLine)
}

// 스페이스 누르면 한페이지 스크롤
function setSpaceEvent(){
    document.addEventListener('keydown',(e)=>{
        if(e.key == ' '){
            clSize = cl.getBoundingClientRect()
            cl.scrollBy({top:(clSize.bottom-clSize.top)*9/10,behavior:'smooth'})
        }
    })
}

// 단락 제목 찾아서 글씨체 바꾸기
function setSection(){
    let lines = document.getElementsByClassName('c_line')
    for(var i in lines){
        var c = lines[i].innerText.toString().trim()
        if(c.startsWith('$$')){
            lines[i].innerText = lines[i].innerText.replace('$$','')
            lines[i].classList.add('c_section') // 제왕절개 아님
        }
    }
}
