const createTodo = async (e) =>{

    // 元々の動作を解除
    e.preventDefault();

    // 入力データの取得
	const title = document.getElementById('input-title').value;
	const description = document.getElementById('input-description').value;

    // サーバーに送信
	const res = await postData(
        "/api/post", 
        {
            "title": title,
            "description": description
        }
    );
    if (!res.ok) {
        alert("Todoの作成に失敗しました");
    }
    
    // 一覧の画面に戻る
    window.location.href = "/"
}

// 送信ボタンを押したときにcreateTodo関数の挙動をさせる
document.querySelector("form.create-todo-form").addEventListener('submit', createTodo);
