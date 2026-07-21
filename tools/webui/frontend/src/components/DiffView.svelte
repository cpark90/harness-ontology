<script>
  // 컬러 unified diff 미리보기(+녹/-적). 서버가 준 문자열을 줄 단위로 분류만 한다.
  export let diff = "";

  $: lines = (diff || "").split("\n").map((l) => {
    let cls = "ctx";
    if (l.startsWith("+") && !l.startsWith("+++")) cls = "add";
    else if (l.startsWith("-") && !l.startsWith("---")) cls = "del";
    return { cls, text: l };
  });
</script>

<pre class="diff">{#each lines as ln}<span class={ln.cls}>{ln.text}</span>{/each}</pre>
