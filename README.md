# valorant-mmr

Use your riot login and password to obtain your competitive results

```
git clone git@github.com:MichaelMarkieta/valorant-mmr-momentum.git
cd valorant-mmr-momentum
```

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```
python3 valorant-mmr-momentum.py

❯ Username: username
❯ Password:
{
    "Version": 0,
    "Subject": "d693ad2b-6026-559d-8c02-df1d943f4c07",
    "Matches": [
        {
            "MatchID": "0afd5204-fa3c-41b7-ad1d-8679f6ced3bb",
            "MapID": "/Game/Maps/Duality/Duality",
            "SeasonID": "d929bc38-4ab6-7da4-94f0-ee84f8ac141e",
            "MatchStartTime": 1646621143462,
            "TierAfterUpdate": 10,
            "TierBeforeUpdate": 10,
            "RankedRatingAfterUpdate": 39,
            "RankedRatingBeforeUpdate": 58,
            "RankedRatingEarned": -19,
            "RankedRatingPerformanceBonus": 0,
            "CompetitiveMovement": "MOVEMENT_UNKNOWN",
            "AFKPenalty": 0
        },
        {
            "MatchID": "59f721c4-dc06-4b7b-a432-50da5819cc8b",
            "MapID": "/Game/Maps/Port/Port",
            "SeasonID": "d929bc38-4ab6-7da4-94f0-ee84f8ac141e",
            "MatchStartTime": 1646617897558,
            "TierAfterUpdate": 10,
            "TierBeforeUpdate": 10,
            "RankedRatingAfterUpdate": 58,
            "RankedRatingBeforeUpdate": 45,
            "RankedRatingEarned": 13,
            "RankedRatingPerformanceBonus": 0,
            "CompetitiveMovement": "MOVEMENT_UNKNOWN",
            "AFKPenalty": 0
        },
        ...
    ]
}
```
