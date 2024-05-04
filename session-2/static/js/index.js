// HTMLの要素を取得
const $getDataBtn = document.getElementById("get-data-btn");
const $outputHello = document.getElementById("output-hello");
const $outputHelloList = document.getElementById("output-hello-list");

// get-data-btnにクリックイベントを追加
$getDataBtn.addEventListener('click', async (event) => {
	/* /helloのAPIにアクセス */
	// データを取得
	const resHello = await fetch("http://localhost:8000/hello");
	// データ取得失敗時に警告を表示
	if (!resHello.ok) {
		alert("データ取得に失敗しました");
	}
	// 送信データ本体を取得
	const dataHello = await resHello.json();
	// "message"のデータを表示
	$outputHello.innerText = dataHello["message"];
});

$getDataBtn.addEventListener('click', async () =>{
	/* /hello-listのAPIにアクセス */
	// データを取得
	const resHelloList = await fetch("http://localhost:8000/hello-list");
	// データ取得失敗時に警告を表示
	if (!resHelloList.ok) {
		alert("データ取得に失敗しました");
	}
	// 送信データ本体を取得
	const dataHelloList = await resHelloList.json();
	// データが複数あるためそれぞれで表示する処理をする
	dataHelloList.forEach((element) => {
		// データを表示する場所を作成
		const $outputElement = document.createElement("div");
		// "message"のデータを表示
		$outputElement.innerText = element["message"];
		// $outputHelloListの中に表示内容を追加
		$outputHelloList.appendChild($outputElement);
	});
});