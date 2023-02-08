import logging


def generateHTML(log, p1name, p2name, p1mons, p2mons):
    p1hps = {mon[0]: 100 for mon in p1mons}
    p1tox = 1
    p2tox = 1
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
    if p1mons[0][1] == "Tyranitar" or p2mons[0][1] == "Tyranitar":
        out.append("|-weather|Sandstorm")
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
                    p1tox = 1
                else:
                    p2active = monname
                    p2tox = 1
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
            elif " fell asleep!" in line:
                parsed = line.split(" fell asleep!")
                parsed = parsed[0].split("'s ")
                isp1 = parsed[0] == p1name
                player = "p1a" if isp1 else "p2a"
                if isp1:
                    p1statuses[parsed[1]] = "slp"
                else:
                    p2statuses[parsed[1]] = "slp"
                out.append("|-status|"+player+": "+parsed[1]+"|slp|")
            elif " was badly poisoned!" in line:
                parsed = line.split(" was badly poisoned!")
                parsed = parsed[0].split("'s ")
                isp1 = parsed[0] == p1name
                player = "p1a" if isp1 else "p2a"
                if isp1:
                    p1statuses[parsed[1]] = "tox"
                else:
                    p2statuses[parsed[1]] = "tox"
                out.append("|-status|"+player+": "+parsed[1]+"|tox|")
            elif "Spikes were scattered all around the feet of " in line:
                target = line.split("Spikes were scattered all around the feet of ")[1].split("'s team!")[0]
                isp1 = target == p1name
                if isp1:
                    out.append("|-sidestart|p1: "+p1name+"|Spikes")
                else:
                    out.append("|-sidestart|p2: "+p2name+"|Spikes")
            elif " was hurt by poison!" in line:
                parsed = line.split(" was hurt by poison!")[0].split("'s ")
                isp1 = parsed[0] == p1name
                if isp1:
                    poisondamage = p1tox
                    p1tox += 1
                else:
                    poisondamage = p2tox
                    p2tox += 1
                player = "p1a" if isp1 else "p2a"
                hps = p1hps if isp1 else p2hps
                newhp = max(hps[parsed[1]] - 6*poisondamage,0)
                hps[parsed[1]] = newhp
                statusdict = p1statuses if isp1 else p2statuses
                out.append("|-damage|"+player+": "+parsed[1]+"|"+str(newhp)+"\/100 "+statusdict[parsed[1]]+"|[from] psn")
            elif " is buffeted by the sandstorm!" in line:
                parsed = line.split(" is buffeted by the sandstorm!")[0].split("'s ")
                isp1 = parsed[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hps = p1hps if isp1 else p2hps
                newhp = max(hps[parsed[1]] - 6,0)
                hps[parsed[1]] = newhp
                statusdict = p1statuses if isp1 else p2statuses
                out.append("|-damage|"+player+": "+parsed[1]+"|"+str(newhp)+"\/100 "+statusdict[parsed[1]]+"|[from] Sandstorm")
            elif " restored a little HP using its Leftovers!" in line:
                parsed = line.split(" restored a little HP using its Leftovers!")[0].split("'s ")
                isp1 = parsed[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hps = p1hps if isp1 else p2hps
                newhp = min(hps[parsed[1]] + 6,100)
                hps[parsed[1]] = newhp
                statusdict = p1statuses if isp1 else p2statuses
                out.append("|-heal|"+player+": "+parsed[1]+"|"+str(newhp)+"\/100 "+statusdict[parsed[1]]+"|[from] item: Leftovers")
            elif "% of its health!" in line:
                parsed = line.split("% of its health!")[0].split(" lost ")
                parsedname = parsed[0].split("'s ")
                isp1 = parsedname[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hps = p1hps if isp1 else p2hps
                newhp = max(hps[parsedname[1]] - int(parsed[1]),0)
                hps[parsedname[1]] = newhp
                statusdict = p1statuses if isp1 else p2statuses
                out.append("|-damage|"+player+": "+parsedname[1]+"|"+str(newhp)+"\/100 "+statusdict[parsedname[1]])
            elif " is hurt by spikes!" in line:
                parsed = line.split(" is hurt by spikes!")[0].split(" lost ")
                parsedname = parsed[0].split("'s ")
                isp1 = parsedname[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hps = p1hps if isp1 else p2hps
                newhp = max(hps[parsedname[1]] - 12,0)
                hps[parsedname[1]] = newhp
                statusdict = p1statuses if isp1 else p2statuses
                out.append("|-damage|"+player+": "+parsedname[1]+"|"+str(newhp)+"\/100 "+statusdict[parsedname[1]])
            elif " was dragged out!" in line:
                parsed = line.split(" was dragged out!")
                parsedname = parsed[0].split("'s ");
                isp1 = parsedname[0] == p1name
                player = "p1a" if isp1 else "p2a"
                hpswitchedin = p1hps if isp1 else p2hps
                statusswitchedin = p1statuses if isp1 else p2statuses
                nickswitchedin = p1nicktospecies if isp1 else p2nicktospecies
                monname = parsedname[1]
                if isp1:
                    p1active = nickswitchedin[monname]
                    p1tox = 1
                else:
                    p2active = nickswitchedin[monname]
                    p2tox = 1
                out.append("|drag|"+player+": "+monname+"|"+nickswitchedin[monname]+"|"+str(hpswitchedin[monname])+"\/100 "+statusswitchedin[monname])







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
