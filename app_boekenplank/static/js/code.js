
var add_review_icon = document.getElementById('add-review-icon')
var add_review_form = document.getElementById('add-review-form')
var close_review_icon = document.getElementById('close-review-icon')

var add_book_icon = document.getElementById('add-book-icon')
var close_book_icon = document.getElementById('close-book-icon')
var add_book_form = document.getElementById('add-book-form')

var add_author_icon = document.getElementById('add-author-icon')
var close_author_icon = document.getElementById('close-author-icon')
var add_author_form = document.getElementById('add-author-form')

var add_publisher_icon = document.getElementById('add-publisher-icon')
var close_publisher_icon = document.getElementById('close-publisher-icon')
var add_publisher_form = document.getElementById('add-publisher-form')



add_review_icon.addEventListener('click', open_review_form)
close_review_icon.addEventListener('click', close_review_form)

add_book_icon.addEventListener('click', open_book_form)
close_book_icon.addEventListener('click', close_book_form)

add_author_icon.addEventListener('click', open_author_form)
close_author_icon.addEventListener('click', close_author_form)

add_publisher_icon.addEventListener('click', open_publisher_form)
close_publisher_icon.addEventListener('click', close_publisher_form)



// <------- Add Review Function ---------->
// Open add review function 
function open_review_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Review OPEN')
    add_review_form.style.display = 'flex'
    close_review_icon.style.display = 'block'
    add_review_icon.style.display = 'none'
}
// Open add book function 
function close_review_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Review CLOSE')
    add_review_form.style.display = 'none'
    close_review_icon.style.display = 'none'
    add_review_icon.style.display = 'block'
}


// <------- Add Book Function ---------->
// Open add review function 
function open_book_form(){
    // add_book_form.style.display = 'flex'
    console.log('-->  BOOK OPEN')
    add_book_form.style.display = 'flex'
    close_book_icon.style.display = 'block'
    add_book_icon.style.display = 'none'

}
// Open add book function 
function close_book_form(){
    // add_book_form.style.display = 'flex'
    console.log(' -->  BOOk  CLOSE')
    add_book_form.style.display = 'none'
    close_book_icon.style.display = 'none'
    add_book_icon.style.display = 'block'

}

// <------- Add Author Function ---------->
// Open add review function 
function open_author_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Author  open')
    add_author_form.style.display = 'flex'
    close_author_icon.style.display = 'block'
    add_author_icon.style.display = 'none'

} 
function close_author_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Author CLOSE')
    add_author_form.style.display = 'none'
    close_author_icon.style.display = 'none'
    add_author_icon.style.display = 'block'

}

// <------- Add Publisher Function ---------->
// Open add review function 
function open_publisher_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Publisher click')
    add_publisher_form.style.display = 'flex'
    close_publisher_icon.style.display = 'block'
    add_publisher_icon.style.display = 'none'

}
// Open add book function 
function close_publisher_form(){
    // add_book_form.style.display = 'flex'
    console.log('--> Publisher CLOSE')
    add_publisher_form.style.display = 'none'
    close_publisher_icon.style.display = 'none'
    add_publisher_icon.style.display = 'block'
}


// var header_wrapper = document.getElementsByClassName("header-wrapper")
// var sticky = header_wrapper.offsetTop;

// window.onscroll = function(){sticky_Heaer()}
