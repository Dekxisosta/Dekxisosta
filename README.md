<table style="border: 0;">
  <tr style="border: 0;"> 
    <td style="border: 0;" rowspan ="3">
        <img src="./banner.png" width="500">
    </td>
    <td style="border: 0;">
        <h1>DEKXISOSTA <br> GITHUB</h1>
        <h6>PROGRAM / UI DESIGN / GAME <br> DEVELOPMENT </h6>
    </td>
    <td style="border: 0;">
        <a href="https://www.discord.com"><img src="./discord.png" width="50"></a>
        <br>
        <a href="https://www.linkedin.com"><img src="./linkedin.png" width="50"></a>
        <br>
        <a href="https://www.x.com/dekxisosta"><img src="./x.png" width="50"></a>
    </td>
    <td style="border: 0;">
        <a href="https://www.youtube.com/@Rroquxii"><img src="./youtube.png" width="50"></a>
        <br>
        <img src="./azurlane_unicorn-cropped.gif" width="50">
        <br>
        <img src="./azurlane_laffey-crop.gif" width="50">
    </td>
  </tr>
</table>

```lua
--Currently learning Luau
function Dekxi.new(isSilly : boolean) : Dekxi
    local self = setmetatable({}, Dekxi)
    self.Actions = {"coding", "designing", "developing"}
    𝗮𝘀𝘀𝗲𝗿𝘁(not isSilly, "I am " .. tostring(self.Actions[math.random(1, #self.Actions)]))
    return self
end
```
