import logging


def generateHTML(log, p1name, p2name, p1mons, p2mons):
    p1hps = {mon[0]: 100 for mon in p1mons}
    p1statuses = {mon[0]: "" for mon in p1mons}
    p2hps = {mon[0]: 100 for mon in p2mons}
    p2statuses = {mon[0]: "" for mon in p2mons}
    p1nicktospecies = {mon[0]: mon[1] for mon in p1mons}
    p2nicktospecies = {mon[0]: mon[1] for mon in p2mons}
    p1active = p1mons[0][0]
    p2active = p2mons[0][0]
    lines = log.split("\n")
    out = []
    out.append(
    """<!DOCTYPE html>
<meta charset="utf-8" />
<!-- version 1 -->
<title>custom replay</title>

<div class="wrapper replay-wrapper" style="max-width: 1180px; margin: 0 auto">
  <div class="battle"></div>
  <div class="battle-log"></div>
  <div class="replay-controls"></div>
  <div class="replay-controls-2"></div>
    <script type="text/plain" class="battle-log-data">
|gametype|singles
|player|p1|"""+p1name+"""|roughneck-gen4|1000
|player|p2|"""+p2name+"""|roughneck-gen4|1000
|teamsize|p1|6
|teamsize|p2|6
|gen|3
|raw|Redless says hi!
|start""")
    out.append("|switch|p1a: "+p1mons[0][0]+"|"+p1mons[0][1]+"|100\/100")
    out.append("|switch|p2a: "+p2mons[0][0]+"|"+p2mons[0][1]+"|100\/100")
    for line in lines:
        try:
            if "Start of turn " in line:
                parsed = line.split("Start of turn ")
                out.append("|turn|"+parsed[1])
            elif " sent out " in line:
                parsed = line.split(" sent out ")
                if "! (" in parsed[1]:
                    monname = parsed[1].split("! (")[0]
                else:
                    monname = parsed[1].split("!")[0]
                isp1 = parsed[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hpswitchedin = p1hps if isp1 else p2hps
                statusswitchedin = p1statuses if isp1 else p2statuses
                nickswitchedin = p1nicktospecies if isp1 else p2nicktospecies
                if isp1:
                    p1active = monname
                else:
                    p2active = monname
                out.append("|switch|"+player+": "+monname+"|"+nickswitchedin[monname]+"|"+str(hpswitchedin[monname])+"\/100 "+statusswitchedin[monname])
            elif " used " in line:
                parsed = line.split(" used ")
                parsedname = parsed[0].split("'s ")
                parsedmove = parsed[1].split("!")
                isp1 = parsedname[0] == p1name
                player = "p1a" if isp1 else "p2a"
                notplayer = "p1a" if not isp1 else "p2a"
                target = p2active if isp1 else p1active
                out.append("|move|"+player+": "+parsedname[1]+"|"+parsedmove[0]+"|"+notplayer+": "+target)
        except Exception as e:
            print("problem line:")
            print(line)
            logging.exception(e)
    out.append(
    """</script>
</div>
<script>
  let daily = Math.floor(Date.now() / 1000 / 60 / 60 / 24);
  document.write(
    '<script src="https://play.pokemonshowdown.com/js/replay-embed.js?version' +
      daily +
      '"></' +
      "script>"
  );
</script>""")
    return "\n".join(out)
