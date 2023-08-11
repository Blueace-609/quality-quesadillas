var modalOpened = false
let images = document.getElementsByClassName("image")
let colleagues = [['Christopher',"I play tennis and Splatoon 3. I am Project Manager, and helped with training the model and Flask",'./static/pictures/christopher.jpg'], ["Tanay", "Enjoys playing tennis and also enhancing his understanding of AI. He helped with dataset generation with API, model training, and some CSS work.", './static/pictures/tanay.jpg'],["Sohma", "I Love playing basketball and chess, and have strong interest in AI/coding! He helped collect data and made our logo.", "./static/pictures/shoma.png"], ["Leo", "He helped with gathering data, making the presentations, and producing our video.", "./static/pictures/IMG_0815.jpg"], ["Aviv", "I really like swimming, playing chess, and coding. I helped with the frontend, the backend, model training, and the css. ", "./static/pictures/aviv.jpeg"], ['Warren', "Hi, I'm Warren, and I love playing the drums and playing games. In this project, my role was being a flexible team member that could do whatever the team needed.", './static/pictures/IMG_0208.png'], ['Mohak', 'Hi, I am Mohak Acharya and I am instructor at AI Camp. Currently I am pursuing my masters in computer science at ASU.','./static/pictures/1581519149843.jpeg']]
colleagues.forEach((col, index)=>{
  images[index].addEventListener("click", modalOpen.bind(col))
})

function modalOpen(){
  let list = this
  console.log(list)
  if(!modalOpened){
    modalOpened = true
    let modal = document.createElement("div")
    modal.classList.add("modal")
    let newh1 = document.createElement("h1")
    newh1.innerHTML = list[0];
    let newP = document.createElement("p")
    newP.innerHTML = list[1];
    let newImg = document.createElement("img")
    newImg.src = list[2];
    let closeButton = document.createElement("button")
    closeButton.innerHTML = "X";
    closeButton.onclick = modalClose;
    modal.append(newh1)
    modal.append(newP)
    modal.append(newImg)
    modal.append(closeButton)
    document.body.append(modal)
    }
}
function modalClose(){
  modalOpened = false;
  document.body.removeChild(document.querySelector(".modal"))
}